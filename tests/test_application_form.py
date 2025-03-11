import pytest
import time
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """Launch Playwright browser once for all tests."""
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False, slow_mo=200)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    """Create a new browser page for each test."""
    page = browser.new_page()
    url = ("https://mostar.demo.melon.market/form/application/new/"
           "bae01d6af78e4420848436fe9d942729/6tb-21c9987501816e557bd8/"
           "67c10f4b-9986-4f94-a90e-4cc6c5e83f6d")
    page.goto(url)
    page.wait_for_selector("body", timeout=20000)
    page.wait_for_timeout(3000)  
    yield page
    page.close()

def test_fill_form(page):
    """Fills Step 1 (Object), navigates to Step 2 (Household), and starts Step 3."""

    click_yes_buttons(page)

    fill_number_inputs(page)

    file_path = "C:/Users/Pc/Pictures/Screenshots/Screenshot 2024-07-04 124108.png"
    upload_and_reupload_file(page, file_path)

    fill_text_fields(page)

    navigate_to_step2(page)

    fill_household_section(page, file_path)

    save_and_next(page)

    add_adult(page)

    fill_step3_personal_info(page)


def test_fill_step3(page):
    """Navigates to Step 3 and fills in personal information."""

    
    url_step3 = ("https://mostar.demo.melon.market/form/application/new/34e0aa24a451410791c134c118783056/6tb-2288c281637e9d1fdfdb/8b4d20d5-93f4-44f8-bec8-a2056c2f2559")  
    page.goto(url_step3)
    
    page.wait_for_selector("body", timeout=20000)
    page.wait_for_timeout(3000)  

    add_adult(page)

    fill_step3_personal_info(page)



def click_yes_buttons(page):
    """Clicks all 'Yes' buttons if not already selected."""
    yes_buttons = page.locator("ul.radio-list li[title='Yes']")
    assert yes_buttons.count() > 0, "No 'Yes' buttons found!"
    for i in range(yes_buttons.count()):
        yes_button = yes_buttons.nth(i)
        if "selected" not in (yes_button.get_attribute("class") or ""):
            yes_button.click()
            time.sleep(0.5)

def navigate_to_step2(page):
    """Clicks 'Save and Next' and waits for Step 2 (Household) to load."""
    save_and_next(page)

    page.wait_for_selector(".af-steps .af-position.active", timeout=15000)
    active_step = page.locator(".af-steps .af-position.active").text_content().strip()
    assert active_step == "2", f"⚠ Not in Step 2! Expected '2', got '{active_step}'"
    

def fill_household_section(page, file_path):
    """Fills in the Household section after navigating to Step 2."""
    page.wait_for_selector(".sections-container", timeout=10000)

    click_yes_buttons(page)

    select_dropdown_option(page, "Household type", "couple household")

    fill_input_field(page, "Type of pet / dog breed", "Golden Retriever")

    upload_and_reupload_file(page, file_path)

    select_radio_option(page, "Music instruments", "Yes")
    fill_input_field(page, "Type of music instrument", "Piano")

    select_radio_option(page, "Smoker", "No")

    select_dropdown_option(page, "Reason for moving", "Change in space requirements")
    fill_input_field(page, "Desired reference date", "01-09-2024")
    fill_input_field(page, "Wanted doorbell/mailbox label", "John Doe")

    select_radio_option(page, "Security deposit (3 grossly month rent)", "Insurance solution")  

    provider_dropdown = page.locator("//span[contains(text(), 'Provider')]")
    if provider_dropdown.count() > 0:
        page.wait_for_selector("//span[contains(text(), 'Provider')]", timeout=5000)
        select_dropdown_option(page, "Provider", "SwissCaution")

    select_radio_option(page, "Monthly household income > 3 monthly rents", "Yes")
    fill_input_field(page, "IBAN number", "CH9300762011623852957")
    fill_input_field(page, "Bank name and location", "Swiss Bank, Zurich")
    fill_input_field(page, "Account owner", "John Doe")

    fill_input_field(page, "Motivation", "Looking for a community-oriented environment.")

    fill_textarea_field(page, "Participation ideas", "Volunteering in community events")
    fill_textarea_field(page, "Remarks", "Looking forward to being part of the community.")

    select_dropdown_option(page, "Object found on", "Search engine")

    select_dropdown_option(page, "Relation to the cooperative", "Current tenant")

    select_dropdown_option(page, "Type of relation", "Already living in the neighborhood")

   
    save_and_next(page)



def fill_textarea_field(page, field_label, value):
    """Fills a textarea field based on the label."""
    
    
    textarea = page.locator(f"//div[contains(@class, 'mdt-textarea')]//div[contains(text(), '{field_label}')]/following::textarea[1]")
    
    if textarea.count() > 0:
        textarea.first.fill(value)
        time.sleep(1)  
    else:
        raise Exception(f"Textarea '{field_label}' not found!")


def select_radio_option(page, field_label, option_text):
    """Selects a radio button based on field label and option text, only if it's not already selected."""
    
    radio_option = page.locator(f"//div[contains(text(), '{field_label}')]/following::li[@title='{option_text}'][1]")

    if radio_option.count() > 0:
        if "selected" not in (radio_option.get_attribute("class") or ""):
            radio_option.first.click()
            time.sleep(1)  
        else:
            print(f" '{field_label}' is already set to '{option_text}', skipping click.")
    else:
        raise Exception(f"Radio option '{option_text}' not found for '{field_label}'!")



def upload_and_reupload_file(page, file_path):
    """Uploads a file, deletes it if already uploaded, then re-uploads it."""
    file_input = page.locator(".mdt-file-upload input[type='file']")
    delete_button = page.locator(".mdt-file-single .icon-delete")

    if file_input.count() > 0:
        page.evaluate("document.querySelector('.mdt-file-upload input[type=file]').style.display = 'block'")

        if delete_button.count() > 0:
            delete_button.click()
            time.sleep(3)

        file_input.set_input_files(file_path)
        time.sleep(3)

def fill_number_inputs(page):
    """Fills number fields and clicks increment/decrement buttons."""
    number_inputs = page.locator(".mdt-number-incrementer input[type='number']")
    
    for i in range(number_inputs.count()):
        number_input = number_inputs.nth(i)
        increment_button = number_input.locator("xpath=../div[@id='increment']")
        decrement_button = number_input.locator("xpath=../div[@id='decrement']")
        
        number_input.fill(str(min(i + 1, 7)))
        time.sleep(0.5)

        if increment_button.count() > 0:
            increment_button.click()
            time.sleep(0.5)

        if decrement_button.count() > 0:
            decrement_button.click()
            time.sleep(0.5)

def fill_text_fields(page):
    """Fills all required text fields."""
    fields = {
        "Car ownership justification": "I own a car for work purposes.",
        "Wanted area of additional room (from-to)": "15-30 sqm",
        "Wanted area of storage room (from-to)": "10-20 sqm",
        "Reason for home office work": "Remote work requirement.",
    }
    
    for label, value in fields.items():
        fill_input_field(page, label, value)

def fill_input_field(page, field_label, value):
    """Fills a single input field based on label."""
    input_field = page.locator(f"//span[contains(text(), '{field_label}')]/ancestor::div[contains(@class, 'mdt-input')]//input")
    if input_field.count() > 0:
        input_field.first.fill(value)
        time.sleep(1)

def select_dropdown_option(page, field_label, option_text):
    """Selects a dropdown option based on the field label."""
    
    dropdown = page.locator(f"//span[contains(text(), '{field_label}')]/ancestor::div[contains(@class, 'mdt-select')]//input")
    if dropdown.count() == 0:
        dropdown = page.locator(f"//label[contains(text(), '{field_label}')]/ancestor::div[contains(@class, 'mdt-select')]//input")

    if dropdown.count() == 0:
        raise Exception(f"Dropdown '{field_label}' not found!")

    dropdown.first.click()
    time.sleep(1.5) 

    page.wait_for_selector("//div[contains(@class, 'text-cut')]", timeout=5000)

    options = page.locator("//div[contains(@class, 'text-cut')]")
    options_count = options.count()

    if options_count > 0:
        for i in range(options_count):
            option = options.nth(i)
            option_text_content = option.text_content().strip().lower()
            if option_text.lower() in option_text_content:
                option.click()
                time.sleep(1) 
                return
        
        print(f" Warning: Option '{option_text}' not found in '{field_label}' dropdown! Clicking first available option.")
        options.first.click() 
        time.sleep(1)
    else:
        raise Exception(f"No options found in '{field_label}' dropdown!")



def save_and_next(page):
    """Clicks 'Save and Next' button if present."""
    save_button = page.locator(".btn-next")
    if save_button.count() > 0:
        save_button.click()
        time.sleep(3)

def add_adult(page):
    """Clicks the 'Add Adult' button at the start of Step 3."""
    add_adult_button = page.locator("//div[contains(@class, 'create-adult')]//i[contains(@class, 'fa-plus-circle')]")
    if add_adult_button.count() > 0:
        add_adult_button.first.click()
        time.sleep(2) 
    else:
        raise Exception("Add Adult button not found!")

def fill_step3_personal_info(page):
    """Fills in personal information (Salutation, Name, Nationality, etc.) in Step 3."""

    select_dropdown_option(page, "Salutation", "Mr.")

    fill_input_field(page, "First name", "John")

    fill_input_field(page, "Last name", "Doe")

    select_date_from_datepicker(page, "Date of birth", "15", "June", "2024")

    fill_input_field(page, "Place of birth", "Zurich")

    select_dropdown_option(page, "Civil status", "single")

    selected_nationality = "Switzerland"  
    select_nationality(page, selected_nationality)

    if selected_nationality == "Switzerland":
        fill_input_field(page, "Hometown", "Bern")  
        print(" Switzerland selected, filled Hometown instead of Residence Permit.")
    else:

        select_residence_permit(page, "(B) Residence permit") 
        print(" Non-Swiss nationality selected, Residence Permit chosen.")

    select_date_from_datepicker(page, "Living in Switzerland since", "19", "January", "2025")

    select_dropdown_option(page, "Type of tenant", "Main tenant")

    fill_phone_number(page, "49", "15234567890")  

    fill_business_phone_number(page, "49", "15234567890")  

    fill_email_fields(page, "20@example.com")

    fill_rental_details(page, "Own home", "123 Main St", "10001")

    fill_location_details(
    page, "Zurich", "Switzerland", "10", "June", "2024", 
    "Yes", "Yes", "Yes",
    prev_street="Old Town 5", prev_postcode="8001", prev_municipality="Zurich",
    entry_day="15", entry_month="May", entry_year="2024", membership_number="123456"
)

    fill_insurance_details(
    page, "Yes", "Swiss Insurance Co.", "Yes", "Premium Home Insurance", "Yes"
)

    fill_employment_and_income_details(
    page, 
    "Tertiary level",  
    "Full-time (90-100%)", 
    "CHF 100’000 - CHF 110’000",  
    85000,  
    120000,  
    occupation="Software Engineer",  
    employment_type="Permanent",  
    start_date="10.10.2024",  
    employment_relationship="Not terminated",  
    company_name="TechCorp Ltd.",  
    street="123 Tech Street",  
    post_code="8000",  
    place_of_work="Zurich",  
    contact_person="John Doe",  
    contact_phone="+41 78 123 45 67",  
    contact_email="20@example.com",
    post_code_index=2 
)       
    fill_credit_check_details(page, file_path="C:/Users/Pc/Pictures/Screenshots/Screenshot 2024-07-04 124108.png")



    confirm_and_save(page)

    check_all_boxes_and_save(page)









    print(" Successfully filled Step 3 Personal Information!")







def select_date_from_datepicker(page, field_label, day, month, year):
    """Selects a date using the datepicker widget by adjusting months."""

    date_input = page.locator(f"//span[contains(text(), '{field_label}')]/ancestor::div[contains(@class, 'mdt-input')]//input")
    if date_input.count() == 0:
        raise Exception(f"Date field '{field_label}' not found!")

    date_input.first.click()
    time.sleep(1)  

    page.wait_for_selector("//div[contains(@class, 'datepicker-wrapper')]", timeout=5000)

    current_date_label = page.locator("//div[contains(@class, 'datepicker-current-date')]")
    
    prev_button = page.locator("//div[contains(@class, 'months-buttons')]/div[1]") 
    next_button = page.locator("//div[contains(@class, 'months-buttons')]/div[2]")  

    max_attempts = 30  
    attempts = 0

    while True:
        current_date_text = current_date_label.text_content().strip()
        if f"{month} {year}" in current_date_text:
            break  

        if f"{year}" not in current_date_text or month not in current_date_text:
            prev_button.click()
        else:
            break 

        time.sleep(0.5)  

        attempts += 1
        if attempts >= max_attempts:
            raise Exception(f"Could not navigate to {month} {year}")

    day_locator = page.locator(f"//td[normalize-space(text())='{day}']")
    if day_locator.count() > 0:
        day_locator.first.click()
        time.sleep(1) 
    else:
        raise Exception(f"Date '{day} {month} {year}' not found in the datepicker!")

    print(f" Successfully selected {day}.{month}.{year}")

def select_nationality(page, country):
    """Searches for and selects a nationality from the dropdown."""
    
    dropdown_button = page.locator("//span[contains(text(), 'Nationality')]/ancestor::div[contains(@class, 'mdt-select')]//i[contains(@class, 'icon-dropdown')]")
    if dropdown_button.count() == 0:
        raise Exception("Nationality dropdown button not found!")
    
    dropdown_button.first.click()
    time.sleep(1)

    search_input = page.locator("//div[contains(@class, 'mdt-select')]//input[@placeholder='Search...']")
    if search_input.count() > 1:
        search_input = search_input.first 

    search_input.fill(country)
    time.sleep(2)  

    page.wait_for_selector("//div[contains(@class, 'text-cut')]", timeout=5000)


    country_option = page.locator(f"//div[contains(@class, 'text-cut') and contains(text(), '{country}')]")
    
    if country_option.count() > 0:
        country_option.first.click()
        time.sleep(1)
        print(f" Successfully selected nationality: {country}")
    else:
    
        search_input.press("Enter")
        print(f" Could not find '{country}' directly, pressed Enter instead.")

def select_residence_permit(page, permit_type):
    """Selects a residence permit from the dropdown."""

    dropdown_wrapper = page.locator("//div[contains(@class, 'mdt-select') and .//span[contains(text(), 'Residence permit')]]")
    
    if dropdown_wrapper.count() == 0:
        raise Exception("Residence permit dropdown container not found!")

    dropdown_wrapper.first.click()  
    time.sleep(1)  

    page.wait_for_selector("//ul[contains(@class, 'select-dropdown-items-wrapper')]", timeout=5000)


    permit_option = page.locator(f"//ul[contains(@class, 'select-dropdown-items-wrapper')]//div[contains(text(), '{permit_type}')]")

    if permit_option.count() > 0:
        permit_option.first.click()
        time.sleep(1)  
        print(f" Successfully selected Residence Permit: {permit_type}")
    else:
        raise Exception(f"Residence permit option '{permit_type}' not found!")

def fill_phone_number(page, country_code, phone_number):
    """Fills in the phone number field with the correct format based on country code."""

    phone_input_wrapper = page.locator("(//div[contains(@class, 'mdt-phone-number-input')])[1]")

    if phone_input_wrapper.count() == 0:
        raise Exception("Phone number input container not found!")

    country_dropdown = phone_input_wrapper.locator(".iti__selected-flag").first
    country_dropdown.click()

    page.wait_for_selector("//ul[contains(@class, 'iti__country-list')]", timeout=5000)

    country_option = page.locator(f"//li[@data-dial-code='{country_code}']").first
    if country_option.count() > 0:
        country_option.click()
        print(f" Successfully selected country code: +{country_code}")
    else:
        raise Exception(f"Country code +{country_code} not found!")

    phone_input = phone_input_wrapper.locator("input.text-cut").first

    formatted_number = format_phone_number(country_code, phone_number)

    phone_input.fill(formatted_number)
    print(f" Successfully entered phone number: {formatted_number}")


def format_phone_number(country_code, phone_number):
    """Formats the phone number according to common patterns for the given country code."""
    country_formats = {
        "41": "XX XXX XX XX",  
        "49": "XXXX XXXXXXX",  
        "33": "X XX XX XX XX",  
        "385": "XX XXX XXXX",  
        "1": "(XXX) XXX-XXXX",  
    }

    if country_code not in country_formats:
        print(f" No predefined format for country code +{country_code}. Using raw input.")
        return phone_number 

    format_mask = country_formats[country_code]
    formatted_number = ""
    num_index = 0

    for char in format_mask:
        if char == "X" and num_index < len(phone_number):
            formatted_number += phone_number[num_index]
            num_index += 1
        else:
            formatted_number += char

    return formatted_number


def fill_business_phone_number(page, country_code, phone_number):
    """Fills in the business phone number field with the correct format based on country code."""
    
    phone_wrappers = page.locator("//div[contains(@class, 'mdt-phone-number-input')]")

    if phone_wrappers.count() < 2:
        raise Exception(" Business phone number input container not found!")

    business_phone_wrapper = phone_wrappers.nth(1)

    country_dropdown = business_phone_wrapper.locator(".iti__selected-flag")
    country_dropdown.click()

    dropdown_list = page.locator("//ul[contains(@class, 'iti__country-list')]").nth(1)
    dropdown_list.wait_for(state="visible", timeout=5000)

    country_option = dropdown_list.locator(f"//li[@data-dial-code='{country_code}']").first
    if country_option.count() > 0:
        country_option.click()
        print(f" Successfully selected business phone country code: +{country_code}")
    else:
        raise Exception(f" Business phone country code +{country_code} not found!")

    phone_input = business_phone_wrapper.locator("input").nth(0)
    if phone_input.count() == 0:
        raise Exception(" Business phone input field not found!")

    formatted_number = format_phone_number(country_code, phone_number)

    phone_input.fill(formatted_number)
    print(f" Successfully entered business phone number: {formatted_number}")

def fill_email_fields(page, email):
    """Fills in the email and confirm email fields."""
    
    email_inputs = page.locator("//input[@type='email']").all()
    
    if len(email_inputs) < 2:
        raise Exception("Email input fields not found!")

    email_inputs[0].fill(email)
    print(f" Successfully entered email: {email}")

    email_inputs[1].fill(email)
    print(f" Successfully confirmed email: {email}")


def fill_rental_details(page, rental_option, street, postcode):
    """Fills in the rental situation, street, and postcode fields."""

    rental_dropdown_wrapper = page.locator("//div[contains(@class, 'mdt-select') and .//span[contains(text(), 'Current rental situation')]]")

    if rental_dropdown_wrapper.count() == 0:
        raise Exception("Rental situation dropdown not found!")

    rental_dropdown = rental_dropdown_wrapper.locator("div.search").first
    rental_dropdown.click()

    page.wait_for_selector("//ul[contains(@class, 'select-dropdown-items-wrapper')]", timeout=5000)

    rental_option_element = page.locator(f"//li[contains(@class, 'dropdown-item') and contains(., '{rental_option}')]").first
    if rental_option_element.count() > 0:
        rental_option_element.click()
        print(f" Selected rental option: {rental_option}")
    else:
        raise Exception(f"Rental option '{rental_option}' not found!")

    street_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Street and Number')]]//input").first
    street_input.fill(street)
    print(f" Entered street: {street}")

    postcode_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Post code')]]//input").first
    postcode_input.fill(str(postcode))
    print(f" Entered postcode: {postcode}")




def fill_location_details(
    page, city, country, move_in_day, move_in_month, move_in_year, 
    principal_residence, relocated, community_member,
    prev_street=None, prev_postcode=None, prev_municipality=None, 
    entry_day=None, entry_month=None, entry_year=None, membership_number=None
):
    """Fills in city, country, move-in date using datepicker, and radio options.
       Also fills additional fields if relocation or community membership is selected as 'Yes'.
    """

    city_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'City')]]//input").first
    city_input.fill(city)
    print(f" Entered city: {city}")

    country_input = page.locator("//div[contains(@class, 'mdt-select') and .//span[contains(text(), 'Country')]]//input").first
    country_input.click()
    country_input.fill(country)
    page.wait_for_selector("//ul[contains(@class, 'select-dropdown-items-wrapper')]", timeout=5000)
    country_option = page.locator(f"//li[contains(@class, 'dropdown-item') and normalize-space(.)='{country}']").first
    if country_option.count() > 0:
        country_option.click()
        page.wait_for_timeout(500)
        page.locator("body").click()
    else:
        raise Exception(f" Country '{country}' not found in dropdown!")

    select_date_from_datepicker(page, "Move-in date", move_in_day, move_in_month, move_in_year)

    page.wait_for_timeout(500)
    page.locator(f"//div[contains(@class, 'mdt-radio-list') and .//div[contains(text(), 'Civil law principal residence')]]//li[contains(text(), '{principal_residence}')]").first.click()
    print(f" Selected Civil law principal residence: {principal_residence}")

    page.wait_for_timeout(500)
    page.locator(f"//div[contains(@class, 'mdt-radio-list') and .//div[contains(text(), 'Relocation in the last 3 years')]]//li[contains(text(), '{relocated}')]").first.click()
    print(f" Selected Relocation in last 3 years: {relocated}")

    if relocated == "Yes":
        fill_input_field(page, "Previous street and number", prev_street)
        fill_input_field(page, "Post code of the previous address", prev_postcode)
        fill_input_field(page, "Previous municipality", prev_municipality)

        date_entry_locator = page.locator("//div[contains(@class, 'mdt-datepicker') and .//span[contains(text(), 'Date of entry')]]//input[@type='text']").first
        if date_entry_locator.count() > 0:
            print(" Found 'Date of entry' field, clicking to open datepicker...")

            date_entry_locator.click()
            page.wait_for_timeout(500)

            page.wait_for_selector("//div[contains(@class, 'datepicker-wrapper')]", timeout=5000)

            try:
                select_date_from_datepicker(page, "Date of entry", entry_day, entry_month, entry_year)
                print(f" Successfully selected Date of Entry: {entry_day}.{entry_month}.{entry_year}")

                page.locator("body").click()
                page.wait_for_timeout(500)
                max_attempts = 5
                attempts = 0
                filled_date = ""

                while attempts < max_attempts:
                    filled_date = date_entry_locator.input_value().strip()
                    if filled_date != "":
                        print(f" 'Date of entry' successfully set: {filled_date}")
                        break
                    time.sleep(1)  
                    attempts += 1

                if filled_date == "":
                    print(" 'Date of entry' field is still empty after selection! Retrying manually...")
                    date_entry_locator.fill(f"{entry_day}.{entry_month}.{entry_year}")
                    page.locator("body").click()
                    page.wait_for_timeout(500)

                    
                    filled_date = date_entry_locator.input_value().strip()
                    if filled_date == "":
                        raise Exception(" 'Date of entry' field is still empty after retrying!")

            except Exception as e:
                print(f" Failed to select 'Date of Entry', skipping. Error: {e}")

        else:
            print(" 'Date of Entry' field not found, skipping.")

    page.wait_for_timeout(500)
    community_radio = page.locator(f"//div[contains(@class, 'mdt-radio-list') and .//div[contains(text(), 'Already a member of the community')]]//li[contains(text(), '{community_member}')]")
    
    if community_radio.count() > 0:
        community_radio.first.click()
        print(f" Selected Community membership: {community_member}")
    else:
        raise Exception(" 'Already a member of the community' field not found!")

    if community_member == "Yes":
        fill_input_field(page, "Membership number", membership_number)
        print(" Filled Membership Number")

    print("⏳ Pausing for 10 seconds so you can verify the selections...")
    time.sleep(3)

def fill_insurance_details(page, liability_insurance, liability_specify, household_insurance, household_specify, free_insurance_check):
    """Fills in the insurance details including personal liability, household insurance, and free insurance check."""

    liability_radio = page.locator(f"//div[contains(@class, 'mdt-radio-list') and .//div[contains(text(), 'Personal liability insurance available')]]//li[contains(text(), '{liability_insurance}')]")
    if liability_radio.count() > 0:
        liability_radio.first.click()
        print(f" Selected Personal Liability Insurance: {liability_insurance}")
    else:
        raise Exception(" 'Personal liability insurance' radio option not found!")

    if liability_insurance == "Yes" and liability_specify:
        fill_input_field(page, "Specify personal liability insurance", liability_specify)
        print(f" Filled Personal Liability Insurance Details: {liability_specify}")

    household_radio = page.locator(f"//div[contains(@class, 'mdt-radio-list') and .//div[contains(text(), 'Household insurance available')]]//li[contains(text(), '{household_insurance}')]")
    if household_radio.count() > 0:
        household_radio.first.click()
        print(f" Selected Household Insurance: {household_insurance}")
    else:
        raise Exception(" 'Household insurance' radio option not found!")

    if household_insurance == "Yes" and household_specify:
        household_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Specify household insurance')]]//input").first
        if household_input.count() > 0:
            household_input.fill(household_specify)
            print(f" Filled Household Insurance Details: {household_specify}")
        else:
            raise Exception(" 'Specify household insurance' input field not found!")

    insurance_check_radio = page.locator(f"//div[contains(@class, 'mdt-radio-list') and .//div[contains(text(), 'Free insurance check wanted')]]//li[contains(text(), '{free_insurance_check}')]")
    if insurance_check_radio.count() > 0:
        insurance_check_radio.first.click()
        print(f" Selected Free Insurance Check: {free_insurance_check}")
    else:
        raise Exception(" 'Free insurance check' radio option not found!")

    print(" Pausing for 5 seconds to visually confirm selections...")
    time.sleep(5)



def fill_employment_and_income_details(page, education_level, employment_status, gross_income, taxable_income, taxable_assets, 
                                       occupation=None, employment_type=None, start_date=None, employment_relationship=None, 
                                       company_name=None, street=None, post_code=None, place_of_work=None, 
                                       contact_person=None, contact_phone=None, contact_email=None,
                                       post_code_index=0):
    """
    Fills in employment details, income, and assets fields. """

    education_dropdown = page.locator("//div[contains(@class, 'mdt-select') and .//span[contains(text(), 'Highest educational qualification')]]")
    if education_dropdown.count() > 0:
        education_dropdown.locator("input").click()
        page.wait_for_selector("//ul[contains(@class, 'select-dropdown-items-wrapper')]", timeout=5000)
        education_option = page.locator(f"//li[contains(@class, 'dropdown-item') and normalize-space(.)='{education_level}']").first
        if education_option.count() > 0:
            education_option.click()
            print(f" Selected Highest Education Level: {education_level}")

    employment_dropdown = page.locator("//div[contains(@class, 'mdt-select') and .//span[contains(text(), 'Employment status')]]")
    if employment_dropdown.count() > 0:
        employment_dropdown.locator("input").click()
        page.wait_for_selector("//ul[contains(@class, 'select-dropdown-items-wrapper')]", timeout=5000)
        employment_option = page.locator(f"//li[contains(@class, 'dropdown-item') and normalize-space(.)='{employment_status}']").first
        if employment_option.count() > 0:
            employment_option.click()
            print(f" Selected Employment Status: {employment_status}")

    if employment_status == "Full-time (90-100%)":
        time.sleep(2)

        occupation_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Occupation')]]//input").first
        if occupation_input.count() > 0 and occupation:
            occupation_input.fill(occupation)
            print(f" Entered Occupation: {occupation}")

        if employment_type:
            employment_type_option = page.locator(f"//li[contains(@class, 'radio-list-item') and normalize-space(text())='{employment_type}']").first
            if employment_type_option.count() > 0:
                employment_type_option.click()
                print(f" Selected Employment Type: {employment_type}")

        start_date_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Starting date at the company')]]//input").first
        if start_date_input.count() > 0 and start_date:
            start_date_input.fill(start_date)
            print(f" Entered Start Date: {start_date}")

        if employment_relationship:
            employment_relationship_option = page.locator(f"//li[contains(@class, 'radio-list-item') and normalize-space(text())='{employment_relationship}']").first
            if employment_relationship_option.count() > 0:
                employment_relationship_option.click()
                print(f" Selected Employment Relationship: {employment_relationship}")

        time.sleep(1)
        permanent_option = page.locator("//li[contains(@class, 'radio-list-item') and normalize-space(text())='Permanent']").first
        if permanent_option.count() > 0:
            permanent_option.click()
            print(" Selected Permanent Employment")

        not_terminated_option = page.locator("//li[contains(@class, 'radio-list-item') and normalize-space(text())='Not terminated']").first
        if not_terminated_option.count() > 0:
            not_terminated_option.click()
            print(" Selected Not Terminated")

        company_name_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Company name')]]//input").first
        if company_name_input.count() > 0 and company_name:
            company_name_input.fill(company_name)
            print(f" Entered Company Name: {company_name}")

        street_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Street and number')]]//input").first
        if street_input.count() > 0 and street:
            street_input.fill(street)
            print(f" Entered Street: {street}")

        post_code_inputs = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Post code')]]//input")
        if post_code and post_code_inputs.count() > post_code_index:
            post_code_input = post_code_inputs.nth(post_code_index)
            print(" Post Code input found, entering value using evaluate on element handle...")

            post_code_input.evaluate(
                """(el, value) => {
                    el.value = value;
                    el.dispatchEvent(new Event('input', { bubbles: true }));
                    el.dispatchEvent(new Event('change', { bubbles: true }));
                }""", str(post_code)
            )
            time.sleep(1)
            current_value = post_code_input.input_value()
            print(f" Post Code after evaluate input: {current_value}")

            if current_value != str(post_code):
                print(" Post Code value did not persist, retrying evaluate...")
                post_code_input.evaluate(
                    """(el, value) => {
                        el.value = value;
                        el.dispatchEvent(new Event('input', { bubbles: true }));
                        el.dispatchEvent(new Event('change', { bubbles: true }));
                    }""", str(post_code)
                )
                time.sleep(1)
                current_value = post_code_input.input_value()
                print(f" Post Code after second evaluate input: {current_value}")
                if current_value != str(post_code):
                    print(" Failed to set post code.")
                else:
                    print(f" Entered Post Code: {post_code}")
            else:
                print(f" Entered Post Code: {post_code}")
        else:
            print(" Post Code input field not found or invalid index!")

        place_of_work_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Place of work')]]//input").first
        if place_of_work_input.count() > 0 and place_of_work:
            place_of_work_input.fill(place_of_work)
            print(f" Entered Place of Work: {place_of_work}")

        contact_person_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Contact person for reference check')]]//input").first
        if contact_person_input.count() > 0 and contact_person:
            contact_person_input.fill(contact_person)
            print(f" Entered Contact Person: {contact_person}")

        contact_phone_input = page.locator("//div[contains(@class, 'mdt-phone-number-input') and .//span[contains(text(), 'Phone number of contact person')]]//input").first
        if contact_phone_input.count() > 0 and contact_phone:
            contact_phone_input.fill(contact_phone)
            print(f" Entered Contact Phone: {contact_phone}")

        contact_email_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Email address of contact person')]]//input").first
        if contact_email_input.count() > 0 and contact_email:
            contact_email_input.fill(contact_email)
            print(f" Entered Contact Email: {contact_email}")

    income_dropdown = page.locator("//div[contains(@class, 'mdt-select') and .//span[contains(text(), 'Gross annual income')]]")
    if income_dropdown.count() > 0:
        income_dropdown.locator("input").click()
        page.wait_for_selector("//ul[contains(@class, 'select-dropdown-items-wrapper')]", timeout=5000)
        income_option = page.locator(f"//li[contains(@class, 'dropdown-item') and normalize-space(.)='{gross_income}']").first
        if income_option.count() > 0:
            income_option.click()
            print(f" Selected Gross Annual Income: {gross_income}")

    taxable_income_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Annual taxable income')]]//input").first
    if taxable_income_input.count() > 0:
        taxable_income_input.fill(str(taxable_income))
        print(f" Entered Annual Taxable Income: {taxable_income}")

    taxable_assets_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Taxable assets')]]//input").first
    if taxable_assets_input.count() > 0:
        taxable_assets_input.fill(str(taxable_assets))
        print(f" Entered Taxable Assets: {taxable_assets}")

    print(" Pausing for 10 seconds to visually confirm selections...")
    time.sleep(10)





    

def fill_credit_check_details(page, file_path):
    """Selects 'Excerpt from the debt collection register' and uploads the file to all required fields."""
    
    credit_check_option = page.locator("//li[contains(@class, 'radio-list-item') and normalize-space(.)='Excerpt from the debt collection register']").first
    if credit_check_option.count() > 0:
        credit_check_option.click()
        print(" Selected Credit Check Type: Excerpt from the debt collection register")

    document_labels = [
        "Excerpt from the debt collection register",
        "Copy of ID or passport",
        "Copy of residence permit",
        "Tax invoice / withholding tax",
        "Additional document",
        "Additional document 2",
        "Additional document 3"
    ]

    for label in document_labels:
        file_input = page.locator(f"//div[contains(@class, 'mdt-file-single') and .//span[contains(text(), '{label}')]]//input[@type='file']").first
        if file_input.count() > 0:
            file_input.set_input_files(file_path)
            print(f" Uploaded file for: {label}")
        else:
            print(f" File input not found for: {label} (Skipping)")

    print(" All required files uploaded successfully.")
    

def confirm_and_save(page):
    """Checks the agreement checkbox, fills in missing Post Code if needed, clicks Save, deletes a user if marked for removal, and then clicks Save and Next."""
    
    agreement_checkbox = page.locator("//input[@id='agreement_references']").first
    if agreement_checkbox.count() > 0 and not agreement_checkbox.is_checked():
        agreement_checkbox.check(force=True)
        print(" Checked agreement confirmation checkbox.")
    else:
        print(" Agreement checkbox already checked or not found.")
    
    post_code_input = page.locator("//div[contains(@class, 'mdt-input') and .//span[contains(text(), 'Post code')]]//input").first
    if post_code_input.count() > 0:
        current_value = post_code_input.input_value()
        if not current_value.strip():
            post_code_input.fill("8000")
            print(" Entered missing Post Code: 8000")
            time.sleep(2) 

    save_button = page.locator("//div[contains(@class, 'btn-primary') and normalize-space(text())='Save']").first
    if save_button.count() > 0:
        save_button.click(force=True)
        print(" Clicked Save button.")
    else:
        print(" Save button not found!")
    
    print(" Waiting 10 seconds for Save to complete...")
    time.sleep(10)
    
    
    person_card = page.locator("div.person-card[section-key='0'][field-key='0'][person-key='0']").first
    if person_card.count() > 0:
        try:
            person_card.hover()
            print(" Hovered over the person card.")
            time.sleep(0.5)
            
            trash_icon = person_card.locator("div.actions i.fa-regular.fa-trash-can").first
            if trash_icon.count() > 0:
                trash_icon.click(force=True)
                print(" Clicked trash icon within the person card.")
            else:
                print(" Trash icon not found within the person card.")
        except Exception as e:
            print(" Exception while hovering or clicking trash icon:", e)
        
        try:
            page.wait_for_selector("div.modal-footer", state="visible", timeout=10000)
            print(" Deletion modal appeared.")
            delete_button = page.locator("div.modal-footer div.btn.confirm-button.btn-danger", has_text="Delete").first
            if delete_button.count() > 0:
                delete_button.click(force=True)
                print(" Clicked Delete button to confirm deletion.")
                time.sleep(2)  
            else:
                print(" Delete button not found in modal.")
        except Exception as e:
            print(" Deletion modal did not appear or failed:", e)
    else:
        print(" No person card found; no deletion needed.")
    
    
    save_next_button = page.locator("//div[contains(@class, 'navigation-buttons')]//div[contains(@class, 'btn-next') and normalize-space(text())='Save and next']").first
    if save_next_button.count() > 0:
        save_next_button.scroll_into_view_if_needed()
        save_next_button.click(force=True)
        print(" Clicked 'Save and Next' button.")
    else:
        print(" 'Save and Next' button not found!")
    
    print(" Waiting 5 seconds for verification...")
    time.sleep(15)


def check_all_boxes_and_save(page):
    """Checks the three agreement checkboxes and clicks the Save button."""
  
    truth_checkbox = page.locator("input#agreement_truth").first
    if truth_checkbox.count() > 0:
        if not truth_checkbox.is_checked():
            truth_checkbox.check(force=True)
            print(" Checked 'Truth' checkbox.")
        else:
            print(" 'Truth' checkbox already checked.")
    else:
        print(" 'Truth' checkbox not found.")
    
    privacy_checkbox = page.locator("input#agreement_privacy").first
    if privacy_checkbox.count() > 0:
        if not privacy_checkbox.is_checked():
            privacy_checkbox.check(force=True)
            print(" Checked 'Privacy' checkbox.")
        else:
            print(" 'Privacy' checkbox already checked.")
    else:
        print(" 'Privacy' checkbox not found.")
    
    penalty_checkbox = page.locator("input#agreement_penalty").first
    if penalty_checkbox.count() > 0:
        if not penalty_checkbox.is_checked():
            penalty_checkbox.check(force=True)
            print(" Checked 'Penalty' checkbox.")
        else:
            print(" 'Penalty' checkbox already checked.")
    else:
        print(" 'Penalty' checkbox not found.")
    
    
    save_button = page.locator("div.btn.btn-next", has_text="Save").first
    if save_button.count() > 0:
        save_button.click(force=True)
        print(" Clicked Save button.")
    else:
        print(" Save button not found.")
    
    time.sleep(7)
