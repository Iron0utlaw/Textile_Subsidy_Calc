from flask import Flask, render_template, request, jsonify
import math

# District and Taluka data from the PDF
DISTRICT_TALUKAS = {
    "Ahmedabad": {
        "Category 1": ["Dholera", "Detroj-Rampura", "Dhandhuka"],
        "Category 2": ["Viramgam", "Bavla", "Dholka", "Sanand", "Mandal"],
        "Category 3": ["Ahmedabad City", "Daskroi"]
    },
    "Amreli": {
        "Category 1": ["Khambha", "Dhari", "Lilia", "Savar Kundla", "Babra", "Kunkavav Vadia", "Lathi"],
        "Category 2": ["Rajula", "Bagasara", "Amreli"],
        "Category 3": ["Jafrabad"]
    },
    "Anand": {
        "Category 1": ["Tarapur", "Anklav", "Sojitra"],
        "Category 2": ["Umreth", "Khambhat", "Borsad", "Petlad"],
        "Category 3": ["Anand"]
    },
    "Arvalli": {
        "Category 1": ["Dhansura", "Malpur"],
        "Category 2": ["Meghraj", "Bayad", "Bhiloda", "Modasa"],
        "Category 3": []
    },
    "Banas Kantha": {
        "Category 1": ["Lakhani", "Amirgadh", "Suigam", "Danta", "Dhanera", "Vav", "Kankrej", "Vadgam", "Tharad", "Deodar", "Dantiwada"],
        "Category 2": ["Deesa", "Bhabhar", "Palanpur"],
        "Category 3": []
    },
    "Bharuch": {
        "Category 1": ["Netrang", "Jambusar", "Valia"],
        "Category 2": ["Amod", "Vagra", "Anklesvar", "Hansot"],
        "Category 3": ["Bharuch", "Jhagadia"]
    },
    "Bhavnagar": {
        "Category 1": ["Jesar", "Umrala", "Vallabhipur", "Gariadhar", "Palitana", "Talaja", "Ghogha"],
        "Category 2": ["Mahuva", "Sihor"],
        "Category 3": ["Bhavnagar"]
    },
    "Botad": {
        "Category 1": ["Ranpur", "Gadhada", "Barwala", "Botad"],
        "Category 2": [],
        "Category 3": []
    },
    "Chhota Udepur": {
        "Category 1": ["Chhota Udepur", "Kavant", "Nasvadi", "Sankheda", "Bodeli", "Jetpur Pavi"],
        "Category 2": [],
        "Category 3": []
    },
    "Devbhumi Dwarka": {
        "Category 1": ["Kalyanpur", "Bhanvad"],
        "Category 2": ["Okhamandal"],
        "Category 3": ["Khambhalia"]
    },
    "Dahod": {
        "Category 1": ["Dhanpur", "Sanjeli", "Limkheda", "Dahod", "Fatepura", "Jhalod", "Singvad", "Garbada", "Devgadhbaria"],
        "Category 2": [],
        "Category 3": []
    },
    "Gandhinagar": {
        "Category 1": ["Mansa"],
        "Category 2": ["Kalol", "Dehgam"],
        "Category 3": ["Gandhinagar"]
    },
    "Gir Somnath": {
        "Category 1": ["Gir Gadhada", "Talala", "Sutrapada"],
        "Category 2": ["Una", "Kodinar", "Veraval"],
        "Category 3": []
    },
    "Jamnagar": {
        "Category 1": ["Jodiya"],
        "Category 2": ["Jamjodhpur", "Kalavad", "Dhrol"],
        "Category 3": ["Lalpur", "Jamnagar"]
    },
    "Junagadh": {
        "Category 1": ["Bhesan", "Mendarda"],
        "Category 2": ["Visavadar", "Malia-Hatina", "Mangrol", "Vanthali", "Manavadar", "Keshod"],
        "Category 3": ["Junagadh", "Junagadh City"]
    },
    "Kachchh": {
        "Category 1": ["Rapar", "Nakhatrana", "Lakhpat"],
        "Category 2": ["Abdasa", "Bhachau", "Bhuj", "Mandvi"],
        "Category 3": ["Mundra", "Anjar", "Gandhidham"]
    },
    "Kheda": {
        "Category 1": ["Galteshwar", "Matar", "Vaso", "Mahudha"],
        "Category 2": ["Mehmedabad", "Kathlal", "Thasra", "Kapadvanj"],
        "Category 3": ["Kheda", "Nadiad"]
    },
    "Mehsana": {
        "Category 1": ["Satlasana", "Jotana", "Kheralu", "Becharaji", "Vadnagar"],
        "Category 2": ["Unjha", "Vijapur", "Visnagar"],
        "Category 3": ["Kadi", "Mehsana"]
    },
    "Mahisagar": {
        "Category 1": ["Khanpur", "Kadana", "Virpur"],
        "Category 2": ["Lunawada", "Balasinor", "Santrampur"],
        "Category 3": []
    },
    "Morbi": {
        "Category 1": ["Maliya"],
        "Category 2": ["Halvad", "Morbi", "Tankara"],
        "Category 3": ["Wankaner"]
    },
    "Narmada": {
        "Category 1": ["Garudeshwar", "Dediapada", "Tilakwada", "Sagbara"],
        "Category 2": ["Nandod"],
        "Category 3": []
    },
    "Navsari": {
        "Category 1": ["Khergam"],
        "Category 2": ["Bansda", "Chikhli", "Jalalpore", "Gandevi"],
        "Category 3": ["Navsari"]
    },
    "Panch Mahals": {
        "Category 1": ["Ghoghamaba", "Morva (Hadaf)", "Jambughoda", "Shehera"],
        "Category 2": ["Godhra", "Kalol"],
        "Category 3": ["Halol"]
    },
    "Patan": {
        "Category 1": ["Saraswati", "Santalpur", "Shankheshwar", "Sami", "Radhanpur", "Harij"],
        "Category 2": ["Sidhpur", "Chanasma"],
        "Category 3": ["Patan"]
    },
    "Porbandar": {
        "Category 1": ["Kutiyana"],
        "Category 2": ["Porbandar", "Ranavav"],
        "Category 3": []
    },
    "Rajkot": {
        "Category 1": ["Vinchhlya", "Jamkandorna"],
        "Category 2": ["Jasdan", "Upleta", "Dhoraji", "Jetpur", "Kotda Sangani", "Gondal"],
        "Category 3": ["Paddhari", "Lodhika", "Rajkot"]
    },
    "Sabar Kantha": {
        "Category 1": ["Poshina", "Vijaynagar", "Khedbrahma"],
        "Category 2": ["Talod", "Vadali", "Idar", "Prantij", "Himatnagar"],
        "Category 3": []
    },
    "Surat": {
        "Category 1": ["Umarpada", "Mahuva"],
        "Category 2": ["Mandvi", "Bardoli", "Palsana", "Chorasi", "Olpad"],
        "Category 3": ["Mangrol", "Kamrej", "Surat City"]
    },
    "Surendranagar": {
        "Category 1": ["Lakhtar", "Chuda", "Muli", "Sayla", "Limbdi", "Dasada", "Chotila"],
        "Category 2": ["Thangadh", "Dhrangadhra"],
        "Category 3": ["Wadhwan"]
    },
    "Tapi": {
        "Category 1": ["Kukarmunda", "Uchchhal", "Nizar", "Dolvan", "Songadh"],
        "Category 2": ["Valod"],
        "Category 3": ["Vyara"]
    },
    "The Dangs": {
        "Category 1": ["Subir", "Waghai", "Ahwa"],
        "Category 2": [],
        "Category 3": []
    },
    "Vadodara": {
        "Category 1": ["Sinor", "Desar"],
        "Category 2": ["Dabhoi", "Karjan", "Padra", "Savli"],
        "Category 3": ["Vaghodia", "Vadodara"]
    },
    "Valsad": {
        "Category 1": ["Kaprada", "Dharampur"],
        "Category 2": [],
        "Category 3": ["Valsad", "Pardi", "Vapi", "Umbergaon"]
    }
}

# Create flattened lists of talukas by category
CATEGORY_1 = []
CATEGORY_2 = []
CATEGORY_3 = []

for district, categories in DISTRICT_TALUKAS.items():
    for taluka in categories.get("Category 1", []):
        CATEGORY_1.append(taluka)
    for taluka in categories.get("Category 2", []):
        CATEGORY_2.append(taluka)
    for taluka in categories.get("Category 3", []):
        CATEGORY_3.append(taluka)

def get_category(taluka):
    if taluka in CATEGORY_1:
        return "Category 1"
    elif taluka in CATEGORY_2:
        return "Category 2"
    elif taluka in CATEGORY_3:
        return "Category 3"
    else:
        return "Category 2"  # Default to Category 2 if not found

def calculate_capital_subsidy_rate(category, activity, machine_type):
    # Old machinery is not eligible for capital subsidy
    if machine_type == "old":
        return 0
    
    # Based on the policy chart
    if category == "Category 1":
        return 0.35 if int(activity) == 1 else 0.20
    elif category == "Category 2":
        return 0.30 if int(activity) == 1 else 0.18
    elif category == "Category 3":
        return 0.20 if int(activity) == 1 else 0.10
    else:
        return 0

def calculate_capital_subsidy(machine_price, category, activity, machine_type):
    if machine_type == "old":
        return 0, "Not eligible for old machinery", 0
    
    rate = calculate_capital_subsidy_rate(category, int(activity), machine_type)
    subsidy_amount = machine_price * rate
    return subsidy_amount, f"{rate*100}% of machine price", rate

def get_interest_subsidy_rate(category, activity, machine_type):
    # Old machinery is not eligible for interest subsidy
    if machine_type == "old":
        return 0
    
    # Based on the policy chart
    if category == "Category 1":
        return 0.07  # 7% for both activities
    elif category == "Category 2":
        return 0.07  # 7% for both activities
    elif category == "Category 3":
        return 0.05  # 5% for both activities
    else:
        return 0

def get_power_tariff_subsidy(category):
    # ₹1.5/unit kWh for Category 1, ₹1/unit for others (converted from $ 0.018 and $ 0.012)
    if category == "Category 1":
        return 1.0
    else:
        return 1.0

def format_currency(amount):
    """Format the number as currency with ₹ symbol"""
    return f"₹{amount:,.2f}"

def check_expansion_eligibility(original_gfci, expansion_amount, machine_investment, production_increase):
    """
    Check if an expansion project meets the eligibility criteria
    
    Args:
        original_gfci: Original investment (GFCI) in rupees
        expansion_amount: Expansion investment amount in rupees
        machine_investment: Amount of expansion investment for machines in rupees
        production_increase: Percentage increase in production capacity (0-100)
        
    Returns:
        tuple: (is_eligible, messages, utilization_required)
            is_eligible: Boolean indicating if eligible
            messages: List of messages explaining the eligibility status
            utilization_required: Boolean indicating if utilization check is required
    """
    messages = []
    is_eligible = True
    utilization_required = True
    
    # Check if expansion amount is at least 25% of original GFCI
    expansion_percentage = (expansion_amount / original_gfci) * 100
    if expansion_percentage < 25:
        is_eligible = False
        messages.append(f"Expansion investment (₹{expansion_amount:,.2f}) is only {expansion_percentage:.1f}% of original investment (₹{original_gfci:,.2f}). Minimum required is 25%.")
    else:
        messages.append(f"✓ Expansion investment is {expansion_percentage:.1f}% of original investment, which meets the 25% minimum requirement.")
    
    # Calculate machine percentage and check if at least 60% of expansion is for machinery
    machine_percentage = (machine_investment / expansion_amount) * 100
    if machine_percentage < 60:
        is_eligible = False
        messages.append(f"Only {machine_percentage:.1f}% (₹{machine_investment:,.2f}) of expansion investment is allocated for machinery. Minimum required is 60%.")
    else:
        messages.append(f"✓ {machine_percentage:.1f}% (₹{machine_investment:,.2f}) of expansion investment is allocated for machinery, which meets the 60% minimum requirement.")
    
    # Check if production capacity increases by at least 25%
    if production_increase < 25:
        is_eligible = False
        messages.append(f"Production capacity increase is only {production_increase:.1f}%. Minimum required is 25%.")
    else:
        messages.append(f"✓ Production capacity will increase by {production_increase:.1f}%, which meets the 25% minimum requirement.")
    
    # Add utilization requirement message
    messages.append("Current production capacity utilization must be at least 75% in any of the last 3 years.")
    
    return is_eligible, messages, utilization_required

app = Flask(__name__)

@app.route('/', methods=['GET'])
def welcome():
    """Render the initial welcome page with project type selection"""
    return render_template('welcome.html')

@app.route('/expansion', methods=['GET', 'POST'])
def expansion():
    """Handle the expansion project form"""
    if request.method == 'POST':
        # Get form data
        original_gfci = float(request.form['original_gfci'])
        expansion_amount = float(request.form['expansion_amount'])
        machine_investment = float(request.form['machine_investment'])
        production_increase = float(request.form['production_increase'])
        utilization = float(request.form.get('utilization', 75))  # Default to 75% if not provided
        
        # Check eligibility
        is_eligible, messages, utilization_required = check_expansion_eligibility(
            original_gfci, expansion_amount, machine_investment, production_increase
        )
        
        # Calculate machine percentage
        machine_percentage = (machine_investment / expansion_amount) * 100 if expansion_amount > 0 else 0
        
        return render_template('expansion.html', 
                              is_eligible=is_eligible, 
                              messages=messages,
                              original_gfci=original_gfci,
                              expansion_amount=expansion_amount,
                              machine_investment=machine_investment,
                              machine_percentage=machine_percentage,
                              utilization_required=utilization_required)
    
    return render_template('expansion.html')

@app.route('/new_unit', methods=['GET'])
def new_unit():
    """Handle the new unit information page"""
    return render_template('new_unit.html')

@app.route('/modernisation', methods=['GET', 'POST'])
def modernisation():
    if request.method == 'POST':
        # Get form data
        original_gfci = float(request.form['original_gfci'])
        modernisation_amount = float(request.form['modernisation_amount'])
        
        # Calculate percentage of investment
        investment_percentage = (modernisation_amount / original_gfci) * 100
        
        # Check eligibility
        is_eligible = investment_percentage >= 25
        
        # Prepare messages
        messages = []
        if investment_percentage >= 25:
            messages.append(f"Investment percentage: {investment_percentage:.1f}% - Meets the minimum 25% requirement")
        else:
            messages.append(f"Investment percentage: {investment_percentage:.1f}% - Does not meet the minimum 25% requirement")
            
        messages.append("Please ensure the old machinery is at least 20 years old")
        messages.append("Please ensure you are upgrading with modern technology")
        messages.append("Please ensure modernisation is happening in the same premises")
        
        return render_template('modernisation.html', 
                              is_eligible=is_eligible,
                              original_gfci=original_gfci,
                              modernisation_amount=modernisation_amount,
                              investment_percentage=investment_percentage,
                              messages=messages)
    
    return render_template('modernisation.html')

@app.route('/calculator', methods=['GET', 'POST'])
def calculator():
    """Main calculator function"""
    if request.method == 'POST':
        # Get form data
        taluka = request.form['taluka']
        activity = request.form['activity']
        investment = float(request.form['investment'])  # Now in absolute rupees
        machine_price = float(request.form['machine_price'])
        machine_type = request.form['machine_type']
        ltv_percentage = float(request.form['ltv_percentage'])
        interest_rate = float(request.form['interest_rate'])
        loan_term = int(request.form['loan_term'])
        cfm_consumption = float(request.form['cfm_consumption'])
        rate_per_unit = float(request.form.get('rate_per_unit', 10.0))  # Default rate per unit in rupees
        rpm = int(request.form['rpm'])
        
        # Get category based on taluka
        category = get_category(taluka)
        
        # Calculate Capital Subsidy
        capital_subsidy, capital_subsidy_text, capital_subsidy_rate = calculate_capital_subsidy(
            machine_price, category, activity, machine_type
        )
        price_after_capital_subsidy = machine_price - capital_subsidy
        
        # Calculate Loan Details
        loan_amount = (machine_price * ltv_percentage) / 100
        
        # Calculate Interest Subsidy
        interest_subsidy_rate = get_interest_subsidy_rate(category, activity, machine_type)
        
        # Calculate Interest Amount
        interest_amount = (interest_subsidy_rate * loan_amount * loan_term)
        
        # Calculate Power consumption
        kwh_per_cfm = cfm_consumption / 6.5  # Calculate kWh per CFM as per requirement
        
        # Set machine consumption based on type
        machine_kwh_consumption = 6 if machine_type == "new" else 4
        
        # Calculate annual units consumed
        daily_consumption = kwh_per_cfm + machine_kwh_consumption
        annual_units_consumed = daily_consumption * 24 * 365
        
        # Calculate electricity bill
        electricity_bill_per_machine = annual_units_consumed * rate_per_unit
        
        # Calculate total machine cost (CS + IS + 5yr electricity)
        total_machine_cost = price_after_capital_subsidy + (electricity_bill_per_machine * 5) + interest_amount
        
        # Prepare result dictionary
        result = {
            'taluka': taluka,
            'category': category,
            'machine_type': 'New' if machine_type == 'new' else 'Old',
            'machine_price': format_currency(machine_price),
            'capital_subsidy_percentage': f"{capital_subsidy_rate * 100:.0f}%",
            'capital_subsidy_amount': format_currency(capital_subsidy),
            'price_after_capital_subsidy': format_currency(price_after_capital_subsidy),
            'ltv_percentage': ltv_percentage,
            'loan_amount': format_currency(loan_amount),
            'loan_term': loan_term,
            'interest_rate': interest_rate,
            'interest_subsidy_rate': f"{interest_subsidy_rate * 100:.1f}%",
            'interest_amount': format_currency(interest_amount),
            'cfm_consumption': cfm_consumption,
            'kwh_per_cfm': kwh_per_cfm,
            'machine_kwh_consumption': machine_kwh_consumption,
            'annual_units_consumed': annual_units_consumed,
            'rate_per_unit': format_currency(rate_per_unit),
            'electricity_bill_per_machine': format_currency(electricity_bill_per_machine),
            'total_machine_cost': format_currency(total_machine_cost),
            'rpm': rpm
        }
        
        return render_template('calculator.html', result=result)
    
    # Pass the district data to the template when rendering the page
    districts = list(DISTRICT_TALUKAS.keys())
    return render_template('calculator.html', districts=districts)

@app.route('/talukas', methods=['GET'])
def get_talukas():
    """API endpoint to get all talukas and their categories"""
    all_talukas = {}
    
    for taluka in CATEGORY_1:
        all_talukas[taluka] = "Category 1"
    
    for taluka in CATEGORY_2:
        all_talukas[taluka] = "Category 2"
    
    for taluka in CATEGORY_3:
        all_talukas[taluka] = "Category 3"
    
    return jsonify(all_talukas)

@app.route('/district_talukas', methods=['GET'])
def get_district_talukas():
    """API endpoint to get the structure of districts and their talukas"""
    return jsonify(DISTRICT_TALUKAS)

@app.route('/talukas_by_district', methods=['GET'])
def get_talukas_by_district():
    """API endpoint to get talukas for a specific district"""
    district = request.args.get('district', '')
    if district in DISTRICT_TALUKAS:
        talukas = {}
        for category, taluka_list in DISTRICT_TALUKAS[district].items():
            for taluka in taluka_list:
                talukas[taluka] = category
        return jsonify(talukas)
    else:
        return jsonify({})

@app.route('/calculate_api', methods=['POST'])
def calculate_api():
    """API endpoint for calculations"""
    data = request.get_json()
    
    # Get input parameters
    taluka = data.get('taluka', '')
    activity = data.get('activity', '1')
    machine_price = float(data.get('machine_price', 0))
    machine_type = data.get('machine_type', 'new')
    ltv_percentage = float(data.get('ltv_percentage', 70))
    interest_rate = float(data.get('interest_rate', 10))
    loan_term = int(data.get('loan_term', 5))
    cfm_consumption = float(data.get('cfm_consumption', 20))
    rate_per_unit = float(data.get('rate_per_unit', 10.0))  # Default in rupees
    rpm = int(data.get('rpm', 800))
    
    # Get category based on taluka
    category = get_category(taluka)
    
    # Calculate Capital Subsidy
    capital_subsidy, _, capital_subsidy_rate = calculate_capital_subsidy(
        machine_price, category, activity, machine_type
    )
    price_after_capital_subsidy = machine_price - capital_subsidy
    
    # Calculate Loan Details
    loan_amount = (machine_price * ltv_percentage) / 100
    
    # Calculate Interest Subsidy
    interest_subsidy_rate = get_interest_subsidy_rate(category, activity, machine_type)
    
    # Calculate Interest Amount
    interest_amount = (interest_subsidy_rate * loan_amount * loan_term)
    
    # Calculate Power consumption
    kwh_per_cfm = cfm_consumption / 6.5  # Calculate kWh per CFM as per requirement
    
    # Set machine consumption based on type
    machine_kwh_consumption = 6 if machine_type == "new" else 4
    
    # Calculate annual units consumed
    daily_consumption = kwh_per_cfm + machine_kwh_consumption
    annual_units_consumed = daily_consumption * 24 * 365
    
    # Calculate electricity bill
    electricity_bill_per_machine = annual_units_consumed * rate_per_unit
    
    # Calculate total machine cost (CS + IS + 5yr electricity)
    total_machine_cost = price_after_capital_subsidy + (electricity_bill_per_machine * 5) + interest_amount
    
    # Prepare result dictionary - returning raw numbers for API
    result = {
        'taluka': taluka,
        'category': category,
        'machine_type': 'New' if machine_type == 'new' else 'Old',
        'machine_price': machine_price,
        'capital_subsidy_percentage': capital_subsidy_rate * 100,
        'capital_subsidy_amount': capital_subsidy,
        'price_after_capital_subsidy': price_after_capital_subsidy,
        'ltv_percentage': ltv_percentage,
        'loan_amount': loan_amount,
        'loan_term': loan_term,
        'interest_rate': interest_rate,
        'interest_subsidy_rate': interest_subsidy_rate * 100,
        'interest_amount': interest_amount,
        'cfm_consumption': cfm_consumption,
        'kwh_per_cfm': kwh_per_cfm,
        'machine_kwh_consumption': machine_kwh_consumption,
        'annual_units_consumed': annual_units_consumed,
        'rate_per_unit': rate_per_unit,
        'electricity_bill_per_machine': electricity_bill_per_machine,
        'total_machine_cost': total_machine_cost,
        'rpm': rpm
    }
    
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)