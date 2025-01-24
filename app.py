from flask import Flask, render_template, request
from model import db, Products, Suppliers
from forms import SearchForm
from sqlalchemy.orm import sessionmaker
from model import populate_sample_data
import google.generativeai as genai
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "MYSECRETKEYHAI"

db.init_app(app)

# Initialize generative AI
genai.configure(api_key=os.getenv("API_KEY"))

generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 500,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-2.0-flash-exp",
    generation_config=generation_config,
)

chat_session = model.start_chat(history=[])


# Define the search function
def search(prompt):
    try:
        # Normalize user input for consistent comparison
        normalized_prompt = prompt.lower().strip()

        # Use app context to access the database
        with app.app_context():
            # Create a new session for the query
            Session = sessionmaker(bind=db.engine)
            session = Session()

            if "laptop" in normalized_prompt:
                # Fetch laptops or products containing "laptop" in their name or category
                products = (
                    session.query(Products)
                    .filter(Products.name.ilike("%laptop%"))
                    .all()
                )
                if products:
                    product_list = [
                        f"{product.name} - {product.brand} - ${product.price}"
                        for product in products
                    ]
                    response = (
                        "Here are some laptops from our database:<br>"
                        + "<br>".join(product_list)
                    )
                else:
                    response = "Sorry, we couldn't find any laptops in the database."
            elif "suppliers" in normalized_prompt:
                # Extract product category from the query
                category = normalized_prompt.split("suppliers for")[-1].strip()
                suppliers = (
                    session.query(Suppliers)
                    .join(Products)
                    .filter(Products.category.ilike(f"%{category}%"))
                    .all()
                )
                if suppliers:
                    supplier_list = [
                        f"{supplier.name} - {supplier.contact_info}"
                        for supplier in suppliers
                    ]
                    response = f"Here are suppliers for {category}:<br>" + "<br>".join(
                        supplier_list
                    )
                else:
                    response = f"Sorry, we couldn't find suppliers for {category}."
            elif "details of product" in normalized_prompt:
                product_name = normalized_prompt.split("details of product")[-1].strip()
                product = (
                    session.query(Products)
                    .filter(Products.name.ilike(f"%{product_name}%"))
                    .first()
                )
                if product:
                    response = f"Details of {product.name}: Brand - {product.brand}, Price - ${product.price}"
                else:
                    response = "Sorry, I couldn't find details for that product."
            else:
                # Fallback to dynamic response from Gemini model
                response = chat_session.send_message(prompt).text.strip()

            session.close()  # Close the session after use

        return response.replace("\n", "<br>")
    except Exception as e:
        return f"Error: {str(e)}"


# Define the home route
@app.route("/", methods=["GET", "POST"])
def home():
    chat_history = []
    form = SearchForm()
    if form.validate_on_submit():
        prompt = form.prompt.data
        chat_history.append({"sender": "you", "text": prompt})

        # Call the extended search function
        response = search(prompt)

        chat_history.append({"sender": "ai", "text": response})

    return render_template("index.html", form=form, chat_history=chat_history)


# Ensure database tables are created
with app.app_context():
    db.create_all()
    populate_sample_data()

if __name__ == "__main__":
    app.run(debug=True)
