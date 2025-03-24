#!/usr/bin/env python3
import sys
from datetime import datetime
from nepali_datetime import date as nepali_date

def get_nepali_day_name(day_number):
    nepali_days = {
    0: "आइतबार",
    1: "सोमबार",
    2: "मंगलबार",
    3: "बुधबार",
    4: "बिहिबार",
    5: "शुक्रबार",
    6: "शनिबार"
    }
    return nepali_days.get(day_number, "")

def get_nepali_month_name(month_number):
    nepali_months = {
        1: "बैशाख",
        2: "जेठ",
        3: "असार",
        4: "श्रावण",
        5: "भदौ",
        6: "आश्विन",
        7: "कार्तिक",
        8: "मंसिर",
        9: "पुष",
        10: "माघ",
        11: "फाल्गुन",
        12: "चैत्र"
    }
    return nepali_months.get(month_number, "")

def to_nepali_numerals(number):
    nepali_numerals = {
        '0': '०',
        '1': '१',
        '2': '२',
        '3': '३',
        '4': '४',
        '5': '५',
        '6': '६',
        '7': '७',
        '8': '८',
        '9': '९'
    }
    return ''.join(nepali_numerals.get(digit, digit) for digit in str(number))

def main():
    # Check if any arguments were provided
    if len(sys.argv) > 1:
        print("Error: This command doesn't accept any arguments.", file=sys.stderr)
        print("Usage: nepdate", file=sys.stderr)
        sys.exit(1)

    try:
        # Get current date
        current_date = datetime.now()
        
        # Convert to Nepali date
        nepali_current = nepali_date.from_datetime_date(current_date.date())
        
        # Get day names
        nepali_day = get_nepali_day_name(nepali_current.weekday())
        english_day = current_date.strftime("%A")
        
        # Get Nepali month name
        nepali_month = get_nepali_month_name(nepali_current.month)
        
        # Format Nepali date with Nepali numerals
        nepali_year = to_nepali_numerals(nepali_current.year)
        nepali_day_num = to_nepali_numerals(nepali_current.day)
        nepali_date_str = f"{nepali_year} साल {nepali_month} {nepali_day_num} गते"
        
        # Format English date
        english_date_str = current_date.strftime("%Y-%m-%d")
        
        print(f"नेपाली मिति: {nepali_day} {nepali_date_str}")
        print(f"English Date: {english_day} {english_date_str}")
        
    except Exception as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main() 