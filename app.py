from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import csv
from io import StringIO
from flask import Response

app = Flask(__name__)

DATABASE = "database.db"


# ==========================================================
# DATABASE CONNECTION
# ==========================================================

def get_db():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ==========================================================
# AI ANALYSIS
# ==========================================================

def ai_analysis(company):

    score = company["lead_score"]
    status = company["financial_status"]
    buying = company["buying_intent"]
    win = company["win_probability"]

    if score >= 95:
        priority = "★★★★★"
        level = "Excellent Lead"
    elif score >= 90:
        priority = "★★★★☆"
        level = "High Potential"
    elif score >= 80:
        priority = "★★★☆☆"
        level = "Good Lead"
    else:
        priority = "★★☆☆☆"
        level = "Needs Follow Up"

    if status == "Profitable":
        finance = "Healthy Financial Position"
    else:
        finance = "Company Running in Loss"

    if buying == "High":
        action = "Schedule Product Demo Immediately"
    elif buying == "Medium":
        action = "Arrange Sales Meeting"
    else:
        action = "Continue Email Campaign"

    if win >= 95:
        risk = "Low"
    elif win >= 85:
        risk = "Medium"
    else:
        risk = "High"

    return {

        "priority": priority,
        "level": level,
        "finance": finance,
        "action": action,
        "risk": risk

    }


# ==========================================================
# DASHBOARD
# ==========================================================

@app.route("/")
def dashboard():

    conn = get_db()

    companies = conn.execute("""

        SELECT *
        FROM companies
        ORDER BY lead_score DESC

    """).fetchall()

    if len(companies) == 0:

        conn.close()

        return render_template(

            "dashboard.html",

            companies=[],
            company=None

        )

    company_id = request.args.get("company")

    if company_id:

        company = conn.execute(

            "SELECT * FROM companies WHERE id=?",

            (company_id,)

        ).fetchone()

    else:

        company = companies[0]

    ai = ai_analysis(company)

    total_companies = len(companies)

    profitable = len(

        [c for c in companies if c["financial_status"] == "Profitable"]

    )

    loss = len(

        [c for c in companies if c["financial_status"] == "Loss"]

    )

    high_priority = len(

        [c for c in companies if c["priority"] == "High"]

    )

    average_score = round(

        sum(c["lead_score"] for c in companies)

        / total_companies

    )

    conn.close()

    return render_template(

        "dashboard.html",

        companies=companies,

        company=company,

        ai=ai,

        total_companies=total_companies,

        profitable=profitable,

        loss=loss,

        high_priority=high_priority,

        average_score=average_score

    )
# ==========================================================
# ADD COMPANY
# ==========================================================

@app.route("/add", methods=["GET", "POST"])
def add_company():

    if request.method == "POST":

        conn = get_db()

        conn.execute("""

        INSERT INTO companies(

        company_name,
        industry,
        contact_person,
        designation,
        email,
        phone,
        website,
        employees,
        revenue,
        expenses,
        profit,
        profit_margin,
        financial_status,
        funding,
        location,
        technology,
        lead_score,
        buying_intent,
        lead_status,
        priority,
        expected_deal,
        follow_up,
        recommendation,
        win_probability,
        growth_rate,
        customer_rating,
        last_contact,
        notes,
        ceo,
        sales_director,
        finance_manager,
        procurement_head

        )

        VALUES
        (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)

        """,

        (

        request.form["company_name"],
        request.form["industry"],
        request.form["contact_person"],
        request.form["designation"],
        request.form["email"],
        request.form["phone"],
        request.form["website"],
        request.form["employees"],
        request.form["revenue"],
        request.form["expenses"],
        request.form["profit"],
        request.form["profit_margin"],
        request.form["financial_status"],
        request.form["funding"],
        request.form["location"],
        request.form["technology"],
        request.form["lead_score"],
        request.form["buying_intent"],
        request.form["lead_status"],
        request.form["priority"],
        request.form["expected_deal"],
        request.form["follow_up"],
        request.form["recommendation"],
        request.form["win_probability"],
        request.form["growth_rate"],
        request.form["customer_rating"],
        request.form["last_contact"],
        request.form["notes"],
        request.form["ceo"],
        request.form["sales_director"],
        request.form["finance_manager"],
        request.form["procurement_head"]

        )

        )

        conn.commit()
        conn.close()

        return redirect(url_for("dashboard"))

    return render_template("add_company.html")


# ==========================================================
# DELETE COMPANY
# ==========================================================

@app.route("/delete/<int:id>")
def delete_company(id):

    conn = get_db()

    conn.execute(

        "DELETE FROM companies WHERE id=?",

        (id,)

    )

    conn.commit()
    conn.close()

    return redirect(url_for("dashboard"))


# ==========================================================
# SEARCH COMPANY
# ==========================================================

@app.route("/search")
def search_company():

    keyword = request.args.get("q", "")

    conn = get_db()

    companies = conn.execute("""

    SELECT *

    FROM companies

    WHERE

    company_name LIKE ?

    OR industry LIKE ?

    OR location LIKE ?

    ORDER BY lead_score DESC

    """,

    (

        "%" + keyword + "%",
        "%" + keyword + "%",
        "%" + keyword + "%"

    )

    ).fetchall()

    if companies:

        company = companies[0]
        ai = ai_analysis(company)

    else:

        company = None
        ai = None

    total_companies = len(companies)

    profitable = len(

        [c for c in companies if c["financial_status"] == "Profitable"]

    )

    loss = len(

        [c for c in companies if c["financial_status"] == "Loss"]

    )

    high_priority = len(

        [c for c in companies if c["priority"] == "High"]

    )

    if total_companies > 0:

        average_score = round(

            sum(c["lead_score"] for c in companies)

            / total_companies

        )

    else:

        average_score = 0

    conn.close()

    return render_template(

        "dashboard.html",

        companies=companies,

        company=company,

        ai=ai,

        total_companies=total_companies,

        profitable=profitable,

        loss=loss,

        high_priority=high_priority,

        average_score=average_score

    )
# ==========================================================
# COMPANY COMPARISON
# ==========================================================

@app.route("/compare")
def compare():

    conn = get_db()

    companies = conn.execute("""

        SELECT *

        FROM companies

        ORDER BY company_name

    """).fetchall()

    id1 = request.args.get("company1")
    id2 = request.args.get("company2")

    company1 = None
    company2 = None

    if id1 and id2:

        company1 = conn.execute(

            "SELECT * FROM companies WHERE id=?",

            (id1,)

        ).fetchone()

        company2 = conn.execute(

            "SELECT * FROM companies WHERE id=?",

            (id2,)

        ).fetchone()

    conn.close()

    return render_template(

        "compare.html",

        companies=companies,

        company1=company1,

        company2=company2

    )


# ==========================================================
# ANALYTICS PAGE
# ==========================================================

@app.route("/analytics")
def analytics():

    conn = get_db()

    companies = conn.execute("""

        SELECT *

        FROM companies

    """).fetchall()

    revenue = []
    profit = []
    names = []

    profitable = 0
    loss = 0

    for c in companies:

        names.append(c["company_name"])

        revenue.append(

            int(
                c["revenue"]
                .replace("₹", "")
                .replace(" Crore", "")
            )
        )

        profit.append(

            abs(
                int(
                    c["profit"]
                    .replace("₹", "")
                    .replace(" Crore", "")
                )
            )

        )

        if c["financial_status"] == "Profitable":

            profitable += 1

        else:

            loss += 1

    conn.close()

    return render_template(

        "analytics.html",

        companies=companies,

        names=names,

        revenue=revenue,

        profit=profit,

        profitable=profitable,

        loss=loss

    )


# ==========================================================
# COMPANY DETAILS
# ==========================================================

@app.route("/company/<int:id>")
def company(id):

    conn = get_db()

    company = conn.execute(

        "SELECT * FROM companies WHERE id=?",

        (id,)

    ).fetchone()

    ai = ai_analysis(company)

    conn.close()

    return render_template(

        "dashboard.html",

        company=company,

        ai=ai,

        companies=[],

        total_companies=0,

        profitable=0,

        loss=0,

        high_priority=0,

        average_score=0

    )
# ==========================================================
# EXPORT COMPANIES TO CSV
# ==========================================================

@app.route("/export")
def export_csv():

    conn = get_db()

    companies = conn.execute("""

        SELECT *

        FROM companies

        ORDER BY lead_score DESC

    """).fetchall()

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([

        "Company",
        "Industry",
        "Contact",
        "Revenue",
        "Expenses",
        "Profit",
        "Financial Status",
        "Lead Score",
        "Buying Intent",
        "Priority",
        "Win Probability"

    ])

    for company in companies:

        writer.writerow([

            company["company_name"],
            company["industry"],
            company["contact_person"],
            company["revenue"],
            company["expenses"],
            company["profit"],
            company["financial_status"],
            company["lead_score"],
            company["buying_intent"],
            company["priority"],
            company["win_probability"]

        ])

    conn.close()

    output.seek(0)

    return Response(

        output,

        mimetype="text/csv",

        headers={

            "Content-Disposition":
            "attachment; filename=salespro_companies.csv"

        }

    )


# ==========================================================
# TOP COMPANIES
# ==========================================================

@app.route("/top")
def top_companies():

    conn = get_db()

    companies = conn.execute("""

        SELECT *

        FROM companies

        ORDER BY lead_score DESC

        LIMIT 5

    """).fetchall()

    conn.close()

    return render_template(

        "dashboard.html",

        companies=companies,

        company=companies[0] if companies else None,

        ai=ai_analysis(companies[0]) if companies else None,

        total_companies=len(companies),

        profitable=len(

            [c for c in companies if c["financial_status"]=="Profitable"]

        ),

        loss=len(

            [c for c in companies if c["financial_status"]=="Loss"]

        ),

        high_priority=len(

            [c for c in companies if c["priority"]=="High"]

        ),

        average_score=round(

            sum(c["lead_score"] for c in companies)/len(companies)

        ) if companies else 0

    )


# ==========================================================
# ERROR PAGE
# ==========================================================

@app.errorhandler(404)
def page_not_found(e):

    return "<h2>404 - Page Not Found</h2>", 404


# ==========================================================
# RUN APPLICATION
# ==========================================================

if __name__ == "__main__":

    app.run(

        debug=True,

        host="0.0.0.0",

        port=5000

    )