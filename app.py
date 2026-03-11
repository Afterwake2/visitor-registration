from flask import Flask, render_template, request, redirect
import psycopg2
import os

app = Flask(__name__)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn


@app.route("/", methods=["GET", "POST"])
def index():

    if request.method == "POST":

        first_name = request.form["first_name"]
        last_name = request.form["last_name"]
        contact_number = request.form["contact_number"]
        company_name = request.form["company_name"]
        purpose = request.form["purpose"]
        contact_person = request.form["contact_person"]

        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO visitors
        (first_name,last_name,contact_number,company_name,purpose_of_visit,contact_person)
        VALUES (%s,%s,%s,%s,%s,%s)
        """, (first_name,last_name,contact_number,company_name,purpose,contact_person))

        conn.commit()

        cur.close()
        conn.close()

        return redirect("/")

    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)