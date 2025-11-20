"""
Remaining 38 states cottage food data
To be integrated into state_compliance_service.py
"""

REMAINING_STATES = {
    # PERMISSIVE STATES (continued)
    "AL": {"state_name": "Alabama", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": [], "training": ["Food safety course required"], "notes": "Very permissive - No sales cap."},
           "home_restaurant_requirements": {"permits": ["Food service permit"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "AZ": {"state_name": "Arizona", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": ["Free registration required"], "training": ["Food handler certification"], "notes": "Can sell to grocery stores."},
           "home_restaurant_requirements": {"permits": ["Food establishment license"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "AR": {"state_name": "Arkansas", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "No permits or training required. Can ship across state lines."},
           "home_restaurant_requirements": {"permits": ["Food service permit"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "ID": {"state_name": "Idaho", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "No permits or special requirements. Low-risk foods only."},
           "home_restaurant_requirements": {"permits": ["Food establishment permit"], "training": ["Food Handler Permit"], "notes": "Commercial requirements."}},
    
    "IA": {"state_name": "Iowa", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 35000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "$35K annual cap. Wide variety of foods."},
           "home_restaurant_requirements": {"permits": ["Food establishment license"], "training": ["Food Protection Manager"], "notes": "Commercial requirements."}},
    
    "KY": {"state_name": "Kentucky", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 50000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "$50K cap. Most non-PHF foods allowed."},
           "home_restaurant_requirements": {"permits": ["Food service establishment permit"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "LA": {"state_name": "Louisiana", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 20000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "$20K cap. Limited food list."},
           "home_restaurant_requirements": {"permits": ["Food establishment permit"], "training": ["Certified Food Manager"], "notes": "Commercial requirements."}},
    
    "MI": {"state_name": "Michigan", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 25000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "$25K cap. Wide variety allowed."},
           "home_restaurant_requirements": {"permits": ["Food service license"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "MS": {"state_name": "Mississippi", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 35000,
           "home_chef_requirements": {"permits": ["Business license"], "training": [], "notes": "$35K cap (recently increased)."},
           "home_restaurant_requirements": {"permits": ["Food establishment permit"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "MT": {"state_name": "Montana", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 50000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "$50K cap. Wide variety allowed."},
           "home_restaurant_requirements": {"permits": ["Food service license"], "training": ["Food Safety Manager"], "notes": "Commercial requirements."}},
    
    "NE": {"state_name": "Nebraska", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": [], "training": ["Accredited food safety course"], "notes": "2024 expansion - Now includes some TCS foods."},
           "home_restaurant_requirements": {"permits": ["Food establishment license"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "NM": {"state_name": "New Mexico", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 75000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "$75K cap. Non-PHF foods."},
           "home_restaurant_requirements": {"permits": ["Food service permit"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "OH": {"state_name": "Ohio", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": ["License required"], "training": [], "notes": "Two license types. Can sell to stores."},
           "home_restaurant_requirements": {"permits": ["Food service operation license"], "training": ["Food Safety Manager"], "notes": "Commercial requirements."}},
    
    "OR": {"state_name": "Oregon", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 50000,
           "home_chef_requirements": {"permits": ["License required ($30)"], "training": [], "notes": "$50K cap. Wide variety allowed."},
           "home_restaurant_requirements": {"permits": ["Food service license"], "training": ["Food Handler Card"], "notes": "Commercial requirements."}},
    
    "PA": {"state_name": "Pennsylvania", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 75000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "One of the most permissive. $75K cap. Can sell through intermediaries."},
           "home_restaurant_requirements": {"permits": ["Food facility license"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "SD": {"state_name": "South Dakota", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "Very extensive - includes some refrigerated foods."},
           "home_restaurant_requirements": {"permits": ["Food establishment license"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "VT": {"state_name": "Vermont", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 125000,
           "home_chef_requirements": {"permits": ["License required ($125)"], "training": [], "notes": "Highest sales cap - $125K. Includes home-cooked meals."},
           "home_restaurant_requirements": {"permits": ["Food service license"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "WV": {"state_name": "West Virginia", "category": "permissive", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 50000,
           "home_chef_requirements": {"permits": [], "training": [], "notes": "$50K cap. Wide variety allowed."},
           "home_restaurant_requirements": {"permits": ["Food establishment permit"], "training": ["Food Safety Manager"], "notes": "Commercial requirements."}},
    
    # MODERATE STATES (continued)
    "CT": {"state_name": "Connecticut", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 25000,
           "home_chef_requirements": {"permits": ["Registration required"], "training": [], "notes": "$25K cap. Pre-approved food list."},
           "home_restaurant_requirements": {"permits": ["Food service establishment license"], "training": ["Food Safety Manager"], "notes": "Commercial requirements."}},
    
    "DE": {"state_name": "Delaware", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 25000,
           "home_chef_requirements": {"permits": ["Registration with health department"], "training": ["Food safety course"], "notes": "$25K cap."},
           "home_restaurant_requirements": {"permits": ["Food establishment license"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "GA": {"state_name": "Georgia", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": ["Business license required"], "training": ["Food safety course required"], "notes": "Home inspection may be required."},
           "home_restaurant_requirements": {"permits": ["Food service establishment permit"], "training": ["Food Safety Manager"], "notes": "Commercial requirements."}},
    
    "IN": {"state_name": "Indiana", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 25000,
           "home_chef_requirements": {"permits": ["Health department registration"], "training": ["Food safety course"], "notes": "$25K cap. Recent updates allow online sales."},
           "home_restaurant_requirements": {"permits": ["Retail food establishment permit"], "training": ["Certified Food Manager"], "notes": "Commercial requirements."}},
    
    "MD": {"state_name": "Maryland", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 50000,
           "home_chef_requirements": {"permits": ["License required"], "training": ["Food safety course"], "notes": "Multiple tiers: $25K for most, $50K for some."},
           "home_restaurant_requirements": {"permits": ["Food service facility license"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "MA": {"state_name": "Massachusetts", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 25000,
           "home_chef_requirements": {"permits": ["License from Dept of Public Health"], "training": ["Food safety course"], "notes": "$25K cap."},
           "home_restaurant_requirements": {"permits": ["Food establishment permit"], "training": ["Food Protection Manager"], "notes": "Commercial requirements."}},
    
    "MN": {"state_name": "Minnesota", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 78000,
           "home_chef_requirements": {"permits": ["Registration required"], "training": ["Safe food handling course"], "notes": "$78K cap (indexed to inflation). Includes some perishables."},
           "home_restaurant_requirements": {"permits": ["Food and beverage service license"], "training": ["Certified Food Manager"], "notes": "Commercial requirements."}},
    
    "NH": {"state_name": "New Hampshire", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 35000,
           "home_chef_requirements": {"permits": ["License required ($25)"], "training": [], "notes": "$35K cap."},
           "home_restaurant_requirements": {"permits": ["Food service establishment license"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "NJ": {"state_name": "New Jersey", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 50000,
           "home_chef_requirements": {"permits": ["Registration required"], "training": [], "notes": "New in 2024 - Last state to allow cottage foods. $50K cap."},
           "home_restaurant_requirements": {"permits": ["Retail food establishment license"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "NV": {"state_name": "Nevada", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 75000,
           "home_chef_requirements": {"permits": ["Health permit required"], "training": [], "notes": "$75K cap."},
           "home_restaurant_requirements": {"permits": ["Food establishment permit"], "training": ["Food Handler Safety Card"], "notes": "Commercial requirements."}},
    
    "NC": {"state_name": "North Carolina", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": None,
           "home_chef_requirements": {"permits": ["May be required depending on product"], "training": ["Depends on product"], "notes": "No comprehensive law - multiple exemptions."},
           "home_restaurant_requirements": {"permits": ["Food service establishment permit"], "training": ["Certified Food Protection Manager"], "notes": "Commercial requirements."}},
    
    "RI": {"state_name": "Rhode Island", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 25000,
           "home_chef_requirements": {"permits": ["License required"], "training": ["Food safety course"], "notes": "$25K cap."},
           "home_restaurant_requirements": {"permits": ["Food establishment license"], "training": ["Food Safety Certification"], "notes": "Commercial requirements."}},
    
    "SC": {"state_name": "South Carolina", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 45000,
           "home_chef_requirements": {"permits": ["Business license"], "training": [], "notes": "$45K cap."},
           "home_restaurant_requirements": {"permits": ["Retail food establishment permit"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
    
    "WA": {"state_name": "Washington", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 35000,
           "home_chef_requirements": {"permits": ["Food worker card required"], "training": ["Food safety training"], "notes": "$35K cap."},
           "home_restaurant_requirements": {"permits": ["Food service establishment permit"], "training": ["Food Protection Manager"], "notes": "Commercial requirements."}},
    
    "WI": {"state_name": "Wisconsin", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 50000,
           "home_chef_requirements": {"permits": ["License required for some tiers"], "training": ["Required for licensed kitchens"], "notes": "Two-tier: $7,500 home-based, $50K licensed."},
           "home_restaurant_requirements": {"permits": ["Restaurant license"], "training": ["Certified Food Manager"], "notes": "Commercial requirements."}},
    
    "DC": {"state_name": "Washington D.C.", "category": "moderate", "cottage_food_allowed": True, "home_dining_allowed": False, "sales_cap": 25000,
           "home_chef_requirements": {"permits": ["Registration required"], "training": ["Food safety course"], "notes": "$25K cap. Recent reforms expanded."},
           "home_restaurant_requirements": {"permits": ["Food establishment license"], "training": ["Food Manager Certification"], "notes": "Commercial requirements."}},
}
