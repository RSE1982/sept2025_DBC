# Importing the MultiPage class from app_pages.multi_page module
from app_pages.multi_page import MultiPage

# Importing the calculator_body function from app_pages.page_calculator module
from app_pages.page_calculator import calculator_body

# Creating an instance of the MultiPage class with the app name "Calculator App"
app = MultiPage(app_name="Calculator App")

# Adding a page named "Calculator" with the calculator_body function as its content
app.add_page("Calculator", calculator_body)

app.run()  # Running the MultiPage app

print("Calculator App is running...")  # Print a message indicating the app is running