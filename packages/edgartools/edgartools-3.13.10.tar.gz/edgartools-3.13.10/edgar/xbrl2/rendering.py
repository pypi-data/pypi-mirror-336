"""
Rendering functions for XBRL data.

This module provides functions for formatting and displaying XBRL data.
"""

from typing import Dict, List, Any, Optional, Tuple, Union

from rich import box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table as RichTable
from rich.text import Text

from edgar.xbrl2.core import (
    determine_dominant_scale, format_value, format_date, parse_date
)
from edgar.xbrl2 import standardization
from edgar.richtools import rich_to_text
from edgar.files.html import Document
from datetime import datetime

share_concepts = [
    'us-gaap_CommonStockSharesOutstanding',
    'us-gaap_WeightedAverageNumberOfSharesOutstandingBasic',
    'us-gaap_WeightedAverageNumberOfSharesOutstandingDiluted',
    'us-gaap_WeightedAverageNumberOfDilutedSharesOutstanding',
    'us-gaap_CommonStockSharesIssued'
]


def _is_html(text: str) -> bool:
    """
    Simple check to determine if a string contains HTML content.
    
    Args:
        text: The string to check
        
    Returns:
        bool: True if the string appears to contain HTML, False otherwise
    """
    html_tags = ['<p', '<div', '<span', '<br', '<table', '<tr', '<td', '<th',
                '<ul>', '<li', '<ol>', '<h1>', '<h2>', '<h3>', '<h4>', '<h5>', '<h6>']
    
    text_lower = text.lower()
    return any(tag in text_lower for tag in html_tags)


def html_to_text(html: str) -> str:
    """
    Convert HTML to plain text.
    
    Args:
        html: HTML content to convert
        
    Returns:
        str: Plain text representation of the HTML
    """
    # Wrap in html tag if not present
    html = f"<html>{html}</html>" if not html.startswith("<html>") else html
    document = Document.parse(html)
    return rich_to_text(document.__str__())


def _format_period_labels(
    periods_to_display: List[Tuple[str, str]], 
    entity_info: Dict[str, Any],
    statement_type: str,
    show_date_range: bool = False
) -> Tuple[List[Tuple[str, str]], Optional[str]]:
    """
    Format period labels for display and determine fiscal period indicator.
    
    This function processes period keys and labels to create human-readable period labels
    for financial statements. When show_date_range=True, duration periods are displayed
    with both start and end dates (e.g., "Jan 1, 2023 - Mar 31, 2023"). When 
    show_date_range=False (default), only the end date is shown (e.g., "Mar 31, 2023").
    
    The function handles various input formats:
    1. Period keys in standard format (instant_YYYY-MM-DD or duration_YYYY-MM-DD_YYYY-MM-DD)
    2. Original labels with full or abbreviated month names
    3. Special formatted labels with date range information
    
    For quarterly periods, quarter numbers (Q1-Q4) are added to provide additional context.
    
    Args:
        periods_to_display: List of period keys and original labels
        entity_info: Entity information dictionary
        statement_type: Type of statement (BalanceSheet, IncomeStatement, etc.)
        show_date_range: Whether to show full date ranges for duration periods
        
    Returns:
        Tuple of (formatted_periods, fiscal_period_indicator)
    """
    formatted_periods = []
    fiscal_period_indicator = None
    
    # Get document_period_end_date from entity_info
    doc_period_end_date = entity_info.get('document_period_end_date')
    
    # First, determine the fiscal period type (annual, quarterly, etc.) based on the first period
    if periods_to_display:
        first_period_key = periods_to_display[0][0]
        
        # For instant periods (Balance Sheet)
        if first_period_key.startswith('instant_'):
            date_str = first_period_key.split('_')[1]
            try:
                date = parse_date(date_str)
                
                # Determine if this is fiscal year end or interim period
                if ('fiscal_year_end_month' in entity_info and 
                    'fiscal_year_end_day' in entity_info and
                    'fiscal_period' in entity_info):
                    
                    fiscal_month = entity_info.get('fiscal_year_end_month')
                    fiscal_day = entity_info.get('fiscal_year_end_day')
                    fiscal_period = entity_info.get('fiscal_period')
                    
                    if fiscal_period == 'FY' or (
                            date.month == fiscal_month and 
                            abs(date.day - fiscal_day) <= 7):
                        fiscal_period_indicator = "Fiscal Year Ended"
                    else:
                        # For quarterly periods
                        if fiscal_period in ['Q1', 'Q2', 'Q3']:
                            month_names = {
                                'Q1': 'First Quarter Ended',
                                'Q2': 'Second Quarter Ended',
                                'Q3': 'Third Quarter Ended'
                            }
                            fiscal_period_indicator = month_names.get(fiscal_period, "Quarter Ended")
                        else:
                            fiscal_period_indicator = "As of"
                else:
                    fiscal_period_indicator = "As of"
            except (ValueError, TypeError):
                fiscal_period_indicator = "As of"
        
        # For duration periods (Income Statement, Cash Flow)
        else:
            start_date_str, end_date_str = first_period_key.split('_')[1], first_period_key.split('_')[2]
            try:
                start_date = parse_date(start_date_str)
                end_date = parse_date(end_date_str)
                duration_days = (end_date - start_date).days
                
                # Determine period type based on duration
                if 85 <= duration_days <= 95:
                    fiscal_period_indicator = "Three Months Ended"
                elif 175 <= duration_days <= 190:
                    fiscal_period_indicator = "Six Months Ended"
                elif 265 <= duration_days <= 285:
                    fiscal_period_indicator = "Nine Months Ended"
                elif 355 <= duration_days <= 375:
                    fiscal_period_indicator = "Year Ended"
                else:
                    # Use fiscal period information if available
                    if 'fiscal_period' in entity_info:
                        fiscal_period = entity_info.get('fiscal_period')
                        if fiscal_period == 'FY':
                            fiscal_period_indicator = "Year Ended"
                        elif fiscal_period == 'Q1':
                            fiscal_period_indicator = "Three Months Ended"
                        elif fiscal_period == 'Q2':
                            fiscal_period_indicator = "Six Months Ended"
                        elif fiscal_period == 'Q3':
                            fiscal_period_indicator = "Nine Months Ended"
                        else:
                            fiscal_period_indicator = "Period Ended"
                    else:
                        fiscal_period_indicator = "Period Ended"
            except (ValueError, TypeError, IndexError):
                fiscal_period_indicator = "Period Ended"
    
    # Create formatted period columns
    for period_key, original_label in periods_to_display:
        # Extract start/end dates from duration periods for date range display
        start_date = None
        end_date = None
        is_duration = False
        duration_days = 0
        q_num = None
        
        # Parse dates from period key for duration periods
        if not period_key.startswith('instant_') and '_' in period_key and len(period_key.split('_')) >= 3:
            parts = period_key.split('_')
            try:
                start_date_str = parts[1]
                end_date_str = parts[2]
                start_date = parse_date(start_date_str)
                end_date = parse_date(end_date_str)
                is_duration = True
                duration_days = (end_date - start_date).days
                
                # Determine quarter number for quarterly periods
                if 80 <= duration_days <= 100:  # Quarterly period
                    month = end_date.month
                    if month <= 3 or month == 12:
                        q_num = "Q1"
                    elif month <= 6:
                        q_num = "Q2"
                    elif month <= 9:
                        q_num = "Q3"
                    else:
                        q_num = "Q4"
            except (ValueError, TypeError, IndexError):
                pass
        # For instant periods, extract the date
        elif period_key.startswith('instant_'):
            try:
                date_str = period_key.split('_')[1]
                end_date = parse_date(date_str)
            except (ValueError, TypeError, IndexError):
                pass

        # Start with the original label or an empty string
        final_label = ""
        
        # First check for date range labels with "to" - prioritize this check
        if original_label and 'to' in original_label:
            # Handle date range labels like "Annual: September 25, 2022 to September 30, 2023"
            try:
                parts = original_label.split(' to ')
                if len(parts) > 1:
                    if show_date_range:
                        # Use the full date range that's already in the label
                        final_label = original_label
                    else:
                        # Extract just the end date when show_date_range is False
                        end_date_str = parts[1].strip()
                        try:
                            end_date = parse_date(end_date_str)
                            final_label = format_date(end_date)
                            
                            # If there's a prefix like "Annual:" or "Q1:", preserve it
                            if ':' in parts[0]:
                                prefix = parts[0].split(':')[0].strip()
                                final_label = f"{prefix}: {final_label}"
                            
                            # Add quarter info if available
                            if q_num and statement_type in ['IncomeStatement', 'CashFlowStatement']:
                                final_label = f"{final_label} ({q_num})"
                        except (ValueError, TypeError):
                            # If we can't parse the end date, use the original label
                            final_label = end_date_str
            except (ValueError, TypeError, IndexError):
                # If any parsing fails, leave label unchanged
                final_label = original_label
        
        # Case 1: If we still don't have a final label and have a date with commas, process it
        elif not final_label and original_label and ',' in original_label:
            for full_month, abbr in [
                ('January', 'Jan'), ('February', 'Feb'), ('March', 'Mar'),
                ('April', 'Apr'), ('May', 'May'), ('June', 'Jun'),
                ('July', 'Jul'), ('August', 'Aug'), ('September', 'Sep'),
                ('October', 'Oct'), ('November', 'Nov'), ('December', 'Dec')
            ]:
                if full_month in original_label:
                    try:
                        # Extract year from the original label
                        year = int(''.join(c for c in original_label.split(',')[1] if c.isdigit()))
                        # Extract day - find digits after the month
                        day_part = original_label.split(full_month)[1].strip()
                        day = int(''.join(c for c in day_part.split(',')[0] if c.isdigit()))
                        month_num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6,
                                   'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}[abbr]
                        
                        try:
                            date_obj = datetime(year, month_num, day).date()
                            final_label = format_date(date_obj)
                            # If showing date range and we have start_date for duration, use it
                            if show_date_range and is_duration and start_date:
                                final_label = f"{format_date(start_date)} - {final_label}"
                            break
                        except ValueError as e:
                            # Handle invalid dates
                            if day > 28:
                                if month_num == 2:  # February
                                    day = 28 if year % 4 != 0 else 29
                                elif month_num in [4, 6, 9, 11]:  # 30-day months
                                    day = 30
                                else:  # 31-day months
                                    day = 31
                                try:
                                    date_obj = datetime(year, month_num, day).date()
                                    final_label = format_date(date_obj)
                                    # If showing date range and we have start_date for duration, use it
                                    if show_date_range and is_duration and start_date:
                                        final_label = f"{format_date(start_date)} - {final_label}"
                                    break
                                except ValueError:
                                    pass
                    except (ValueError, IndexError):
                        pass
            
            # If we couldn't extract a date but label has abbreviated month, use the original
            if not final_label:
                for abbr in ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']:
                    if abbr in original_label:
                        final_label = original_label
                        break
                
                # If no month abbreviation was found, use original label
                if not final_label:
                    final_label = original_label
        
        # Case 2: Handle other special formatted period labels like those with colons
        elif original_label and len(original_label) > 4 and not final_label:
            if ':' in original_label:
                # Labels with prefix like "Annual:" but without "to"
                final_label = original_label
            else:
                # Any other labels we couldn't handle
                final_label = original_label
        
        # Case 3: Either use existing final_label (possibly from Case 1/2) or extract from period key
        # If final_label is set but we want date range for a duration period, check if we need to add the start date
        if final_label and show_date_range and is_duration and start_date and end_date:
            # Check if the final_label already includes a date range (contains a hyphen)
            if "-" not in final_label:
                # If it's not already a date range, it's likely just the end date
                # Try to detect if the label contains the formatted end date
                end_date_formatted = format_date(end_date)
                if end_date_formatted in final_label:
                    # Replace the end date with the full range
                    full_range = f"{format_date(start_date)} - {end_date_formatted}"
                    final_label = final_label.replace(end_date_formatted, full_range)
                else:
                    # If we can't detect the end date pattern, prepend the start date
                    final_label = f"{format_date(start_date)} - {final_label}"
                    
                # If we have quarter info, ensure it's present for income/cash flow statements
                if q_num and statement_type in ['IncomeStatement', 'CashFlowStatement'] and f"({q_num})" not in final_label:
                    final_label = f"{final_label} ({q_num})"
        
        # If we don't have a final_label yet, process based on period key
        if not final_label:
            if period_key.startswith('instant_'):
                # For instant periods, just use the date
                if end_date:
                    final_label = format_date(end_date)
                else:
                    final_label = original_label
            elif is_duration:
                # For duration periods, format based on show_date_range
                if show_date_range and start_date and end_date:
                    final_label = f"{format_date(start_date)} - {format_date(end_date)}"
                    
                    # Add quarter info if available
                    if q_num and statement_type in ['IncomeStatement', 'CashFlowStatement']:
                        final_label = f"{final_label} ({q_num})"
                elif end_date:
                    final_label = format_date(end_date)
                    
                    # Add quarter info if available
                    if q_num and statement_type in ['IncomeStatement', 'CashFlowStatement']:
                        final_label = f"{final_label} ({q_num})"
                else:
                    final_label = original_label
            else:
                # Fall back to original label for anything else
                final_label = original_label
        
        # Add the formatted period to the result
        formatted_periods.append((period_key, final_label))
    
    return formatted_periods, fiscal_period_indicator


def _create_units_note(
    is_monetary_statement: bool, 
    dominant_scale: int, 
    shares_scale: Optional[int]
) -> str:
    """
    Create the units note for the statement title.
    
    Args:
        is_monetary_statement: Whether the statement contains monetary values
        dominant_scale: The dominant scale for monetary values
        shares_scale: The scale for share values, if present
        
    Returns:
        str: Formatted units note or empty string
    """
    if not is_monetary_statement:
        return ""
        
    monetary_scale_text = ""
    if dominant_scale == -3:
        monetary_scale_text = "thousands"
    elif dominant_scale == -6:
        monetary_scale_text = "millions"
    elif dominant_scale == -9:
        monetary_scale_text = "billions"
    
    shares_scale_text = ""
    if shares_scale is not None:
        if shares_scale == -3:
            shares_scale_text = "thousands"
        elif shares_scale == -6:
            shares_scale_text = "millions"
        elif shares_scale == -9:
            shares_scale_text = "billions"
        elif shares_scale == 0:
            shares_scale_text = "actual amounts"
        else:
            # For other negative scales (like -4, -5, -7, etc.)
            # Use a more generic description based on the scale
            scale_factor = 10 ** (-shares_scale)
            if scale_factor >= 1000:
                shares_scale_text = f"scaled by {scale_factor:,}"
    
    # Construct appropriate units note
    if monetary_scale_text and shares_scale_text and shares_scale != dominant_scale:
        return f"[italic](In {monetary_scale_text}, except shares in {shares_scale_text})[/italic]"
    elif monetary_scale_text:
        return f"[italic](In {monetary_scale_text}, except per share data)[/italic]"
    else:
        return ""


def _format_value_for_display(
    value: Any, 
    item: Dict[str, Any], 
    period_key: str, 
    is_monetary_statement: bool,
    dominant_scale: int,
    shares_scale: Optional[int]
) -> Text:
    """
    Format a value for display in a financial statement.
    
    Args:
        value: The value to format
        item: The statement line item containing the value
        period_key: The period key for this value
        is_monetary_statement: Whether this is a monetary statement
        dominant_scale: The dominant scale for monetary values
        shares_scale: The scale for share values, if present
        
    Returns:
        Text: Formatted value as a Rich Text object
    """
    if not isinstance(value, (int, float, str)) or value == "":
        return Text("", justify="right")
        
    # Extract metadata
    concept = item.get('concept', '')
    label = item.get('label', '')
    label_lower = label.lower()
    fact_decimals = item.get('decimals', {}).get(period_key, 0)
    
    # Determine if this is a monetary value
    is_monetary = is_monetary_statement
    is_share_value = False
    
    # Check for share-related values by examining concept names
    if concept in ['us-gaap_EarningsPerShareBasic', 'us-gaap_EarningsPerShareDiluted']:
        is_monetary = False
    elif concept in share_concepts:
        is_monetary = False
        is_share_value = True
    
    # Ratio-related items should not be monetary
    if any(keyword == word for keyword in ['ratio', 'percentage', 'per cent']
           for word in label_lower.split()):
        is_monetary = False
    
    # Format numeric values
    if isinstance(value, (int, float)):
        # Handle share values differently
        if is_share_value and isinstance(fact_decimals, int):
            # Use fact_decimals to determine the appropriate scaling for share values
            # This ensures correct display for companies of all sizes
            if fact_decimals <= -3:
                # Apply appropriate scaling based on the actual decimals value
                scale_factor = 10 ** (-fact_decimals)
                scaled_value = value / scale_factor
                # Always display share amounts with 0 decimal places for cleaner presentation
                return Text(f"{scaled_value:,.0f}", justify="right")
            else:
                # For smaller numbers or positive decimals, use unscaled values
                return Text(f"{value:,.0f}", justify="right")
        else:
            # Format other values normally using the flexible format_value function
            return Text(format_value(value, is_monetary, dominant_scale, fact_decimals), justify="right")
    else:
        # Non-numeric values - check if it's HTML and convert if needed
        if isinstance(value, str) and _is_html(value):
            return Text(html_to_text(value))
        else:
            return Text(str(value), justify="right")


def render_statement(
    statement_data: List[Dict[str, Any]],
    periods_to_display: List[Tuple[str, str]],
    statement_title: str,
    statement_type: str,
    entity_info: Dict[str, Any] = None,
    standard: bool = True,
    show_date_range: bool = False,
) -> RichTable:
    """
    Render a financial statement as a rich table.
    
    Args:
        statement_data: Statement data with items and values
        periods_to_display: List of period keys and labels
        statement_title: Title of the statement
        statement_type: Type of statement (BalanceSheet, IncomeStatement, etc.)
        entity_info: Entity information (optional)
        standard: Whether to use standardized concept labels (default: True)
        show_date_range: Whether to show full date ranges for duration periods (default: False)
        
    Returns:
        RichTable: A formatted table representation of the statement
    """
    entity_info = entity_info or {}
    
    # Apply standardization if requested
    if standard:
        # Create a concept mapper with default mappings
        mapper = standardization.ConceptMapper(standardization.initialize_default_mappings())
        
        # Add statement type to context for better mapping
        for item in statement_data:
            item['statement_type'] = statement_type
        
        # Standardize the statement data
        statement_data = standardization.standardize_statement(statement_data, mapper)
        
        # Update facts with standardized labels if XBRL instance is available
        xbrl_instance = entity_info.get('xbrl_instance')
        if xbrl_instance and hasattr(xbrl_instance, 'facts_view'):
            facts_view = xbrl_instance.facts_view
            facts = facts_view.get_facts()
            
            # Create a mapping of concept -> standardized label from statement data
            standardization_map = {}
            for item in statement_data:
                if 'concept' in item and 'label' in item and 'original_label' in item:
                    if item.get('is_dimension', False):
                        continue
                    standardization_map[item['concept']] = {
                        'label': item['label'],
                        'original_label': item['original_label']
                    }
            
            # Update facts with standardized labels
            for fact in facts:
                if 'concept' in fact and fact['concept'] in standardization_map:
                    mapping = standardization_map[fact['concept']]
                    if fact.get('label') == mapping.get('original_label'):
                        # Store original label if not already set
                        if 'original_label' not in fact:
                            fact['original_label'] = fact['label']
                        # Update with standardized label
                        fact['label'] = mapping['label']
            
            # Clear the cache to ensure it's rebuilt with updated facts
            facts_view.clear_cache()
        
        # Indicate that standardization is being used in the title
        statement_title = f"{statement_title} (Standardized)"
    
    # Create the table
    table = RichTable(title=statement_title, box=box.SIMPLE)
    
    # Determine if this is likely a monetary statement
    is_monetary_statement = statement_type in ['BalanceSheet', 'IncomeStatement', 'CashFlowStatement']
    
    # Format period headers and determine fiscal period indicator
    formatted_periods, fiscal_period_indicator = _format_period_labels(
        periods_to_display, entity_info, statement_type, show_date_range
    )
    
    # Determine the dominant scale for monetary values in this statement
    dominant_scale = determine_dominant_scale(statement_data, periods_to_display)
    
    # Determine the scale used for share amounts if present
    shares_scale = None
    # Look for share-related concepts to determine their scaling from the decimals attribute
    for item in statement_data:
        concept = item.get('concept', '')
        if concept in share_concepts:
            # Check decimals attribute to determine proper scaling
            for period_key, _ in periods_to_display:
                decimals = item.get('decimals', {}).get(period_key)
                if isinstance(decimals, int) and decimals <= 0:
                    # Use the decimals attribute to determine the scale
                    # For shares, decimals is typically negative
                    # -3 means thousands, -6 means millions, etc.
                    shares_scale = decimals
                    break
            if shares_scale is not None:
                break
                
    # Add the fiscal period indicator and note as a subtitle if available
    if formatted_periods:
        subtitles = []
        
        # Add fiscal period indicator if available
        if fiscal_period_indicator:
            subtitles.append(f"[bold]{fiscal_period_indicator}[/bold]")
        
        # Add units note
        units_note = _create_units_note(is_monetary_statement, dominant_scale, shares_scale)
        if units_note:
            subtitles.append(units_note)
        
        # Apply subtitles to table title
        if subtitles:
            table.title = f"{statement_title}\n{' '.join(subtitles)}"
    
    # Extract period metadata for each period for better filtering
    period_metadatas = []
    for period_key, period_label in formatted_periods:
        # Try to extract dates from the period key
        if period_key.startswith('instant_'):
            try:
                date_str = period_key.split('_')[1]
                date = parse_date(date_str)
                period_metadatas.append({
                    'key': period_key,
                    'label': period_label,
                    'type': 'instant',
                    'date': date,
                    'end_date': date,  # Use same date as end_date for comparison
                    'has_metadata': True
                })
                continue
            except (ValueError, TypeError, IndexError):
                pass
        elif '_' in period_key and len(period_key.split('_')) >= 3:
            try:
                parts = period_key.split('_')
                start_date_str = parts[1]
                end_date_str = parts[2]
                start_date = parse_date(start_date_str)
                end_date = parse_date(end_date_str)
                duration_days = (end_date - start_date).days
                period_metadatas.append({
                    'key': period_key,
                    'label': period_label,
                    'type': 'duration',
                    'start_date': start_date,
                    'end_date': end_date,
                    'duration_days': duration_days,
                    'has_metadata': True
                })
                continue
            except (ValueError, TypeError, IndexError):
                pass
        
        # If we get here, we couldn't extract meaningful metadata
        period_metadatas.append({
            'key': period_key,
            'label': period_label,
            'type': 'unknown',
            'has_metadata': False
        })
        
    # Calculate data density for each period
    period_value_counts = {period_key: 0 for period_key, _ in formatted_periods}
    period_item_counts = {period_key: 0 for period_key, _ in formatted_periods}
    
    # Count non-empty values for each period
    for item in statement_data:
        # Skip abstract items as they typically don't have values
        if item.get('is_abstract', False):
            continue
        
        # Skip items with brackets in labels (usually axis/dimension items)
        if any(bracket in item['label'] for bracket in ['[Axis]', '[Domain]', '[Member]', '[Line Items]', '[Table]', '[Abstract]']):
            continue
        
        for period_key, _ in formatted_periods:
            # Count this item for the period
            period_item_counts[period_key] += 1
            
            # Check if it has a value
            value = item['values'].get(period_key)
            if value not in (None, "", 0):  # Consider 0 as a value for financial statements
                period_value_counts[period_key] += 1
    
    # Calculate percentage of non-empty values for each period
    for metadata in period_metadatas:
        period_key = metadata['key']
        count = period_item_counts.get(period_key, 0)
        if count > 0:
            data_density = period_value_counts.get(period_key, 0) / count
        else:
            data_density = 0
            
        metadata['data_density'] = data_density
        metadata['num_values'] = period_value_counts.get(period_key, 0)
        metadata['total_items'] = count
        
    # Use helper function to filter periods by data density
    filtered_periods = [(m['key'], m['label'])
                        for m in period_metadatas
                        if m.get('data_density', 0) > 0
                        ]
    
    # Add columns with right-alignment for numeric columns
    table.add_column("", justify="left")
    for _, period_label in filtered_periods:
        table.add_column(period_label)
    
    # Add rows
    for index, item in enumerate(statement_data):
        # Skip rows with no values if they're abstract (headers without data)
        # But keep abstract items with children (section headers)
        has_children = item.get('children') or item.get('has_dimension_children', False)
        if not item.get('has_values', False) and item.get('is_abstract') and not has_children:
            continue
            
        # Skip non-abstract items without values (missing data)
        if not item.get('has_values', False) and not item.get('is_abstract') and not item.get('children'):
            continue
            
        # Skip axis/dimension items (they contain brackets in their labels)
        if any(bracket in item['label'] for bracket in ['[Axis]', '[Domain]', '[Member]', '[Line Items]', '[Table]', '[Abstract]']):
            continue
            
        # Format the label based on level and abstract status
        level = item['level']

        # Remove [Abstract] from label if present
        label = item['label'].replace(' [Abstract]', '')
        
        # Get values for each period
        period_values = []
        for period_key, _ in filtered_periods:
            value = item['values'].get(period_key, "")
            formatted_value = _format_value_for_display(
                value, item, period_key, 
                is_monetary_statement, dominant_scale, shares_scale
            )
            period_values.append(formatted_value)
        
        # Apply different formatting based on level, abstract status and dimension status
        if item.get('is_dimension', False):
            # Format dimension items with the appropriate style
            indent = "  " * level
            
            # Get dimension metadata if available for more nuanced formatting
            dim_metadata = item.get('dimension_metadata')
            
            # If it's a dimension with just one dimension (most common case),
            # use a cleaner format with just the member name
            if dim_metadata and len(dim_metadata) == 1:
                # Format for single dimension items
                styled_label = f"{indent}[italic]{label}[/italic]"
            else:
                # Format for multi-dimension items (keep full dimension:member notation)
                styled_label = f"{indent}[italic]{label}[/italic]"
                
            table.add_row(styled_label, *period_values)
        elif item['is_abstract']:
            if level == 0:
                # Top-level header - full caps, bold
                styled_label = f"[bold]{label.upper()}[/bold]"
            elif level == 1:
                # Section header - bold
                styled_label = f"[bold]{label}[/bold]"
            else:
                # Sub-section header - indented, bold
                indent = "  " * (level - 1)  # Less aggressive indentation
                styled_label = f"[bold]{indent}{label}[/bold]"
            
            # Headers typically don't have values
            table.add_row(styled_label, *["" for _ in filtered_periods])
        else:
            # Regular line items - indented based on level
            indent = "  " * level
            # If this item has dimension children, make it bold and add a colon
            if item.get('has_dimension_children', False) and item['has_values']:
                styled_label = f"[bold]{indent}{label}:[/bold]"
            else:
                styled_label = f"{indent}{label}"
            table.add_row(styled_label, *period_values)
    
    return table


def generate_rich_representation(xbrl) -> Panel:
    """
    Generate a rich representation of the XBRL document.
    
    Args:
        xbrl: XBRL object
        
    Returns:
        Panel: A formatted panel with XBRL document information
    """
    components = []
    
    # Entity information
    if xbrl.entity_info:
        entity_table = RichTable(title="Entity Information", box=box.SIMPLE)
        entity_table.add_column("Property")
        entity_table.add_column("Value")
        
        for key, value in xbrl.entity_info.items():
            entity_table.add_row(key, str(value))
        
        components.append(entity_table)
    
    # Statements summary
    statements = xbrl.get_all_statements()
    if statements:
        statement_table = RichTable(title="Financial Statements", box=box.SIMPLE)
        statement_table.add_column("Type")
        statement_table.add_column("Definition")
        statement_table.add_column("Elements")
        
        for stmt in statements:
            statement_table.add_row(
                stmt['type'] or "Other",
                stmt['definition'],
                str(stmt['element_count'])
            )
        
        components.append(statement_table)
    
    # Facts summary
    fact_table = RichTable(title="Facts Summary", box=box.SIMPLE)
    fact_table.add_column("Category")
    fact_table.add_column("Count")
    
    fact_table.add_row("Total Facts", str(len(xbrl.facts)))
    fact_table.add_row("Contexts", str(len(xbrl.contexts)))
    fact_table.add_row("Units", str(len(xbrl.units)))
    fact_table.add_row("Elements", str(len(xbrl.element_catalog)))
    
    components.append(fact_table)
    
    # Reporting periods
    if xbrl.reporting_periods:
        period_table = RichTable(title="Reporting Periods", box=box.SIMPLE)
        period_table.add_column("Type")
        period_table.add_column("Period")
        
        for period in xbrl.reporting_periods:
            if period['type'] == 'instant':
                period_table.add_row("Instant", period['date'])
            else:
                period_table.add_row("Duration", f"{period['start_date']} to {period['end_date']}")
        
        components.append(period_table)
    
    return Panel(Group(*components), title="XBRL Document", border_style="green")
