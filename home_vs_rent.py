def calculate_monthly_mortgage(principal, annual_rate, years):
    """Calculates the fixed monthly principal and interest payment."""
    if annual_rate == 0:
        return principal / (years * 12)
    
    monthly_rate = annual_rate / 12
    num_payments = years * 12
    payment = principal * (monthly_rate * (1 + monthly_rate)**num_payments) / ((1 + monthly_rate)**num_payments - 1)
    return payment

def rent_vs_buy_calculator(
    home_price, 
    down_payment_pct, 
    mortgage_rate, 
    mortgage_years,
    property_tax_rate, 
    maintenance_rate, 
    home_appreciation_rate, 
    closing_costs_pct,
    monthly_rent, 
    rent_inflation_rate, 
    investment_return_rate, 
    years_to_compare
):
    """Compares the net worth of buying vs renting over a given time period."""
    
    # --- INITIAL COSTS ---
    down_payment = home_price * down_payment_pct
    closing_costs = home_price * closing_costs_pct
    principal = home_price - down_payment
    
    monthly_mortgage = calculate_monthly_mortgage(principal, mortgage_rate, mortgage_years)
    
    # --- TRACKERS ---
    current_home_value = home_price
    current_rent = monthly_rent
    remaining_mortgage = principal
    
    # If renting, you invest the cash you would have spent on the down payment and closing costs
    rent_investment_portfolio = down_payment + closing_costs
    
    total_rent_paid = 0
    total_buy_sunk_costs = closing_costs # Sunk costs: taxes, maintenance, interest, closing costs
    
    for year in range(1, years_to_compare + 1):
        # -- BUYING MATH --
        annual_property_tax = current_home_value * property_tax_rate
        annual_maintenance = current_home_value * maintenance_rate
        
        # Calculate interest vs principal for the year
        annual_interest = 0
        annual_principal = 0
        for _ in range(12):
            if remaining_mortgage > 0:
                interest_payment = remaining_mortgage * (mortgage_rate / 12)
                principal_payment = monthly_mortgage - interest_payment
                if principal_payment > remaining_mortgage:
                    principal_payment = remaining_mortgage
                annual_interest += interest_payment
                annual_principal += principal_payment
                remaining_mortgage -= principal_payment
        
        # Total cost out of pocket for the buyer this year
        annual_buy_cash_out = annual_interest + annual_principal + annual_property_tax + annual_maintenance
        total_buy_sunk_costs += annual_property_tax + annual_maintenance + annual_interest
        
        # Home appreciates
        current_home_value *= (1 + home_appreciation_rate)

        # -- RENTING MATH --
        annual_rent = current_rent * 12
        total_rent_paid += annual_rent
        
        # The renter invests the difference in monthly cash flow
        # If buying costs $3000/mo and rent is $2000/mo, the renter invests the $1000/mo difference.
        annual_cash_flow_difference = annual_buy_cash_out - annual_rent
        
        # Portfolio grows by the investment return rate, plus the cash flow difference added evenly (approximated at year end)
        rent_investment_portfolio = (rent_investment_portfolio * (1 + investment_return_rate)) + (annual_cash_flow_difference * (1 + (investment_return_rate / 2)))
        
        # Rent increases for next year
        current_rent *= (1 + rent_inflation_rate)

    # --- FINAL NET WORTH CALCULATION ---
    # Buyer's Net Worth: Home value minus remaining mortgage, minus costs to sell (assuming 6% agent fees)
    selling_costs = current_home_value * 0.06
    buyer_net_worth = current_home_value - remaining_mortgage - selling_costs
    
    # Renter's Net Worth: Total value of the investment portfolio
    renter_net_worth = rent_investment_portfolio

    # --- OUTPUT RESULTS ---
    print("="*45)
    print(f" RENT VS BUY FINANCIAL COMPARISON ({years_to_compare} YEARS)")
    print("="*45)
    print(f"Buying Scenario:")
    print(f"  Final Home Value:         ${current_home_value:,.2f}")
    print(f"  Remaining Mortgage:       ${remaining_mortgage:,.2f}")
    print(f"  Estimated Selling Costs:  ${selling_costs:,.2f}")
    print(f"  Total Sunk Costs:         ${total_buy_sunk_costs:,.2f}")
    print(f"  BUYER FINAL NET WORTH:    ${buyer_net_worth:,.2f}")
    print("-" * 45)
    print(f"Renting Scenario:")
    print(f"  Final Monthly Rent:       ${current_rent:,.2f}")
    print(f"  Total Rent Paid:          ${total_rent_paid:,.2f}")
    print(f"  RENTER FINAL NET WORTH:   ${renter_net_worth:,.2f}")
    print("=" * 45)
    
    if buyer_net_worth > renter_net_worth:
        difference = buyer_net_worth - renter_net_worth
        print(f"🏆 BUYING wins by ${difference:,.2f}")
    else:
        difference = renter_net_worth - buyer_net_worth
        print(f"🏆 RENTING wins by ${difference:,.2f}")
    print("=" * 45)

# ==========================================
# ENTER YOUR SCENARIO PARAMETERS HERE
# ==========================================
rent_vs_buy_calculator(
    home_price=450000,              # Purchase price of the home
    down_payment_pct=0.20,          # 20% down payment
    mortgage_rate=0.065,            # 6.5% mortgage interest rate
    mortgage_years=30,              # 30-year fixed mortgage
    property_tax_rate=0.012,        # 1.2% annual property tax
    maintenance_rate=0.01,          # 1% annual maintenance cost
    home_appreciation_rate=0.035,   # 3.5% annual home value growth
    closing_costs_pct=0.03,         # 3% of home price in closing costs
    monthly_rent=2200,              # Cost of renting a similar home
    rent_inflation_rate=0.04,       # Rent increases by 4% per year
    investment_return_rate=0.07,    # 7% average stock market return
    years_to_compare=10             # How long you plan to live there
)