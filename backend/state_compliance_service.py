"""
State Compliance Service
50-state cottage food law and home dining regulations
"""
from typing import Dict, List, Optional, Any
from user_types_models import UserType, StateCategory, StateRegulation
from datetime import datetime


class StateComplianceService:
    """Service for state-specific compliance requirements"""
    
    def __init__(self):
        self.states_data = self._initialize_50_states()
    
    def _initialize_50_states(self) -> Dict[str, Dict[str, Any]]:
        """Initialize all 50 states with compliance data"""
        
        return {
            # FOOD FREEDOM STATES
            "WY": {
                "state_name": "Wyoming",
                "category": StateCategory.FOOD_FREEDOM,
                "cottage_food_allowed": True,
                "home_dining_allowed": True,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Food Freedom State - Minimal regulation. Direct sales to informed consumers."
                },
                "home_restaurant_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Food Freedom State - Can serve meals with minimal oversight."
                },
                "health_dept_url": "https://health.wyo.gov/publichealth/",
            },
            
            "ND": {
                "state_name": "North Dakota",
                "category": StateCategory.FOOD_FREEDOM,
                "cottage_food_allowed": True,
                "home_dining_allowed": True,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Food Freedom State - No revenue caps, minimal licensing."
                },
                "home_restaurant_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Food Freedom State - Broad exemptions for home dining."
                },
                "health_dept_url": "https://www.ndhealth.gov/",
            },
            
            "UT": {
                "state_name": "Utah",
                "category": StateCategory.FOOD_FREEDOM,
                "cottage_food_allowed": True,
                "home_dining_allowed": True,
                "sales_cap": 15000,  # $15K for cottage food, unlimited for food freedom
                "home_chef_requirements": {
                    "permits": ["Business license if >$5,000/year"],
                    "training": [],
                    "notes": "Dual system - cottage food law AND food freedom law."
                },
                "home_restaurant_requirements": {
                    "permits": ["Business license"],
                    "training": [],
                    "notes": "Food Freedom provisions allow home dining with minimal regulation."
                },
                "health_dept_url": "https://ag.utah.gov/",
            },
            
            "ME": {
                "state_name": "Maine",
                "category": StateCategory.FOOD_FREEDOM,
                "cottage_food_allowed": True,
                "home_dining_allowed": True,
                "sales_cap": 50000,
                "home_chef_requirements": {
                    "permits": ["License required ($50)"],
                    "training": [],
                    "notes": "Very extensive allowed foods including some perishables."
                },
                "home_restaurant_requirements": {
                    "permits": ["License"],
                    "training": [],
                    "notes": "Can sell to restaurants. Food sovereignty law also applies."
                },
                "health_dept_url": "https://www.maine.gov/dacf/",
            },
            
            "OK": {
                "state_name": "Oklahoma",
                "category": StateCategory.FOOD_FREEDOM,
                "cottage_food_allowed": True,
                "home_dining_allowed": True,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Homemade Food Freedom Act - Minimal requirements."
                },
                "home_restaurant_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Food Freedom allows broad home food operations."
                },
                "health_dept_url": "https://oklahoma.gov/health.html",
            },
            
            "AK": {
                "state_name": "Alaska",
                "category": StateCategory.FOOD_FREEDOM,
                "cottage_food_allowed": True,
                "home_dining_allowed": True,
                "sales_cap": 100000,  # $25K for some, $100K for others
                "home_chef_requirements": {
                    "permits": ["Business license"],
                    "training": [],
                    "notes": "2024 HB 251 - Broad exemptions from state oversight."
                },
                "home_restaurant_requirements": {
                    "permits": ["Business license"],
                    "training": [],
                    "notes": "New 2024 law allows extensive home food operations."
                },
                "health_dept_url": "http://dhss.alaska.gov/",
            },
            
            # PERMISSIVE STATES
            "TX": {
                "state_name": "Texas",
                "category": StateCategory.PERMISSIVE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Very permissive cottage food law. No permits or training required."
                },
                "home_restaurant_requirements": {
                    "permits": ["Commercial kitchen license", "Health permit"],
                    "training": ["Food Manager Certification"],
                    "notes": "Requires commercial setup for meal service."
                },
                "health_dept_url": "https://www.dshs.texas.gov/",
            },
            
            "FL": {
                "state_name": "Florida",
                "category": StateCategory.PERMISSIVE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": 250000,
                "home_chef_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "One of the most permissive - $250K cap, no permits."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food service establishment license"],
                    "training": ["Food Manager Certification"],
                    "notes": "Requires commercial license for dining service."
                },
                "health_dept_url": "https://www.floridahealth.gov/",
            },
            
            "MO": {
                "state_name": "Missouri",
                "category": StateCategory.PERMISSIVE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "Very permissive - No sales cap, no permits."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food establishment permit"],
                    "training": ["Food Handler Certification"],
                    "notes": "Commercial requirements for meal service."
                },
                "health_dept_url": "https://health.mo.gov/",
            },
            
            "TN": {
                "state_name": "Tennessee",
                "category": StateCategory.PERMISSIVE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": [],
                    "training": [],
                    "notes": "No sales cap or permits required."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food service establishment permit"],
                    "training": ["Food Safety Certification"],
                    "notes": "Requires commercial kitchen for dining service."
                },
                "health_dept_url": "https://www.tn.gov/health.html",
            },
            
            "CO": {
                "state_name": "Colorado",
                "category": StateCategory.PERMISSIVE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": 25000,  # Varies by product
                "home_chef_requirements": {
                    "permits": ["Business license may be required"],
                    "training": [],
                    "notes": "2024 HB 1190 allows refrigerated foods."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food establishment license"],
                    "training": ["Food Handler Certification"],
                    "notes": "Commercial license required for meal service."
                },
                "health_dept_url": "https://cdphe.colorado.gov/",
            },
            
            # MODERATE STATES
            "IL": {
                "state_name": "Illinois",
                "category": StateCategory.MODERATE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": 36000,
                "home_chef_requirements": {
                    "permits": ["Cottage Food Registration (local health dept)", "CFPM Certification"],
                    "training": ["Certified Food Protection Manager (ANSI-accredited)"],
                    "cost": "$0-50/year registration",
                    "notes": "2022 Home-to-Market Act - Very expansive allowed foods list."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food Service Sanitation License", "Business License"],
                    "training": ["Food Manager Certification", "Food Handler Training"],
                    "cost": "$100-1000/year",
                    "notes": "Requires commercial kitchen for dining service."
                },
                "health_dept_url": "https://dph.illinois.gov/topics-services/food-safety/cottage-food.html",
            },
            
            "CA": {
                "state_name": "California",
                "category": StateCategory.MODERATE,
                "cottage_food_allowed": True,
                "home_dining_allowed": True,  # Via MEHKO in some counties
                "sales_cap": 75000,
                "home_chef_requirements": {
                    "permits": ["Class A (direct sales) or Class B (indirect sales) permit"],
                    "training": ["Food Handler Card"],
                    "cost": "$100-200/year",
                    "notes": "Complex system with county-level variations."
                },
                "home_restaurant_requirements": {
                    "permits": ["MEHKO permit (Microenterprise Home Kitchen Operation)"],
                    "training": ["Food Manager Certification"],
                    "cost": "$200-400/year",
                    "notes": "MEHKO allows up to 30 meals/day, 90/week. County must opt-in. $100K sales cap."
                },
                "health_dept_url": "https://www.cdph.ca.gov/Programs/CEH/DFDCS/Pages/FDBPrograms/FoodSafetyProgram/MicroenterpriseHomeKitchenOperations.aspx",
            },
            
            "NY": {
                "state_name": "New York",
                "category": StateCategory.MODERATE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": 50000,
                "home_chef_requirements": {
                    "permits": ["Varies by county"],
                    "training": ["Food safety course (2 hours minimum)"],
                    "notes": "Regulations vary significantly by county."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food service establishment permit"],
                    "training": ["Food Protection Course"],
                    "notes": "Requires commercial kitchen and permits."
                },
                "health_dept_url": "https://www.health.ny.gov/",
            },
            
            "VA": {
                "state_name": "Virginia",
                "category": StateCategory.MODERATE,
                "cottage_food_allowed": True,
                "home_dining_allowed": False,
                "sales_cap": 100000,
                "home_chef_requirements": {
                    "permits": ["Registration required"],
                    "training": ["Food safety course"],
                    "notes": "Two tiers with different limits and allowed foods."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food establishment permit"],
                    "training": ["Food Manager Certification"],
                    "notes": "Commercial requirements for dining service."
                },
                "health_dept_url": "https://www.vdh.virginia.gov/",
            },
            
            # RESTRICTIVE STATES
            "HI": {
                "state_name": "Hawaii",
                "category": StateCategory.RESTRICTIVE,
                "cottage_food_allowed": False,
                "home_dining_allowed": False,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": ["Must use commercial kitchen"],
                    "training": ["Food Handler Certification"],
                    "notes": "No cottage food law as of 2024. Commercial kitchen required."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food establishment permit", "Commercial kitchen"],
                    "training": ["Food Safety Manager Certification"],
                    "notes": "Strict requirements - commercial kitchen mandatory."
                },
                "health_dept_url": "https://health.hawaii.gov/",
            },
            
            "KS": {
                "state_name": "Kansas",
                "category": StateCategory.RESTRICTIVE,
                "cottage_food_allowed": False,  # No comprehensive law
                "home_dining_allowed": False,
                "sales_cap": None,
                "home_chef_requirements": {
                    "permits": ["Limited exemptions exist"],
                    "training": [],
                    "notes": "No comprehensive cottage food law. Check with state agriculture department."
                },
                "home_restaurant_requirements": {
                    "permits": ["Food service establishment license"],
                    "training": ["Food Safety Certification"],
                    "notes": "Commercial requirements apply."
                },
                "health_dept_url": "https://www.kdheks.gov/",
            },
        }
        
        }
        
        # Import and merge remaining states
        from remaining_states_data import REMAINING_STATES
        self.states_data.update(REMAINING_STATES)
        
        return self.states_data
    
    def get_state_info(self, state_code: str) -> Optional[Dict[str, Any]]:
        """Get state compliance information"""
        return self.states_data.get(state_code.upper())
    
    def get_requirements_for_user_type(self, state_code: str, user_type: UserType) -> Dict[str, Any]:
        """Get specific requirements for user type in state"""
        state_info = self.get_state_info(state_code)
        
        if not state_info:
            return {"error": "State not found"}
        
        if user_type == UserType.HOME_CHEF:
            return {
                "state": state_info["state_name"],
                "category": state_info["category"],
                "allowed": state_info["cottage_food_allowed"],
                "requirements": state_info["home_chef_requirements"],
                "sales_cap": state_info["sales_cap"],
                "health_dept_url": state_info.get("health_dept_url")
            }
        
        elif user_type == UserType.HOME_RESTAURANT:
            return {
                "state": state_info["state_name"],
                "category": state_info["category"],
                "allowed": state_info["home_dining_allowed"],
                "requirements": state_info["home_restaurant_requirements"],
                "health_dept_url": state_info.get("health_dept_url")
            }
        
        else:
            return {
                "state": state_info["state_name"],
                "category": state_info["category"],
                "requirements": {"permits": [], "training": [], "notes": "No state requirements."},
                "health_dept_url": state_info.get("health_dept_url")
            }
    
    def get_all_states(self) -> List[Dict[str, str]]:
        """Get list of all states"""
        return [
            {"code": code, "name": data["state_name"], "category": data["category"]}
            for code, data in self.states_data.items()
        ]
    
    def is_food_freedom_state(self, state_code: str) -> bool:
        """Check if state is food freedom"""
        state_info = self.get_state_info(state_code)
        return state_info and state_info["category"] == StateCategory.FOOD_FREEDOM


# Initialize global service
state_compliance_service = StateComplianceService()
