// Internationalization (i18n) configuration for Lambalia
import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';

// Translation resources
const resources = {
  en: {
    translation: {
      // Navigation
      nav: {
        browse: "Browse Templates",
        create: "Create Snippet", 
        ingredients: "Find Ingredients",
        restaurant: "Open Kitchen",
        marketplace: "Local Market",
        charity: "Give Back",
        eats: "Quick Eats",
        offers: "Local Offers",
        profile: "Profile"
      },
      
      // Browse Templates
      browseTemplates: {
        title: "Traditional Recipe Templates",
        subtitle: "Choose from {count} countries with hundreds of authentic recipes",
        searchPlaceholder: "Search recipes or ingredients...",
        allCountries: "All Countries (80+)",
        keyIngredients: "Key Ingredients:",
        culturalNote: "Cultural Note:",
        featured: "Featured",
        useTemplate: "Use This Template",
        difficulty: "Difficulty",
        estimatedTime: "Estimated Time",
        servingSize: "Serving Size",
        recipes: "recipes",
        moreIngredients: "more"
      },

      // Common
      common: {
        loading: "Loading...",
        submit: "Submit",
        cancel: "Cancel",
        save: "Save",
        edit: "Edit",
        delete: "Delete",
        search: "Search",
        filter: "Filter",
        sort: "Sort",
        back: "Back",
        next: "Next",
        previous: "Previous",
        close: "Close",
        open: "Open",
        yes: "Yes",
        no: "No",
        ok: "OK",
        error: "Error",
        success: "Success",
        warning: "Warning",
        info: "Information",
        viewMore: "View More",
        readMore: "Read More",
        showLess: "Show Less",
        noResults: "No results found",
        selectOption: "Select an option",
        pleaseWait: "Please wait...",
        tryAgain: "Try again"
      },

      // Authentication
      auth: {
        login: "Login",
        register: "Register",
        logout: "Logout",
        email: "Email",
        password: "Password",
        username: "Username",
        fullName: "Full Name",
        postalCode: "Postal Code",
        phoneNumber: "Phone Number",
        forgotPassword: "Forgot Password?",
        rememberMe: "Remember Me",
        loginButton: "Enter Your Kitchen 👨‍🍳",
        registerButton: "Join Community",
        joinLambalia: "Join Lambalia",
        welcomeMessage: "Join our community of home chefs sharing authentic recipes from around the world!",
        alreadyHaveAccount: "Already have an account?",
        dontHaveAccount: "Don't have an account?",
        createAccount: "Create Account",
        signIn: "Sign In"
      },

      // Home
      home: {
        title: "Lambalia",
        subtitle: "Taste the World's Heritage",
        welcomeMessage: "Join our community of home chefs sharing authentic recipes from around the world!",
        description: "Connect with passionate home chefs, discover authentic recipes, and turn your kitchen into a global culinary experience.",
        getStarted: "Get Started",
        learnMore: "Learn More",
        features: {
          recipes: "198+ Traditional Recipes",
          monetize: "Monetize Your Cooking Skills",
          restaurant: "Home Restaurant Platform",
          communities: "80+ Cultural Communities",
          heritageRecipes: "Heritage Recipes",
          specialtyIngredients: "Specialty Ingredients"
        },
        actions: {
          browseName: "📚 Browse Templates",
          createName: "✨ Create Snippet", 
          ingredientsName: "🛒 Find Ingredients",
          restaurantName: "🏠👩‍🍳 Open Kitchen",
          marketplaceName: "🌱🛒 Local Market",
          charityName: "🤝❤️ Give Back",
          eatsName: "🚚🍽️ Quick Eats",
          offersName: "🔍 Local Offers"
        },
        cookingClasses: {
          title: "Cooking Classes Online",
          description: "Learn from master chefs around the world",
          learnMore: "Learn More"
        },
        recipeSnippets: {
          title: "Latest Recipe Snippets",
          subtitle: "Quick cooking tips from our community",
          viewAll: "View All Snippets",
          cookingTip: "Cooking Tip",
          noSnippets: "No recipe snippets found. Be the first to share your traditional recipe snippet on Lambalia!"
        },
        communityStats: {
          title: "Join Our Global Culinary Community",
          activeChefs: "Active Home Chefs",
          countriesServed: "Countries Served",
          recipesShared: "Recipes Shared",
          culturesRepresented: "Cultures Represented"
        }
      },

      // Forms
      forms: {
        createSnippet: {
          title: "Create Recipe Snippet",
          recipeTitle: "Recipe Title",
          recipeTitlePlaceholder: "Enter recipe name",
          localTitle: "Local Title",
          localTitlePlaceholder: "Recipe name in your local language (optional)",
          description: "Description",
          descriptionPlaceholder: "Describe your recipe",
          snippetType: "Snippet Type",
          ingredients: "Ingredients",
          ingredientName: "Ingredient",
          amount: "Amount",
          unit: "Unit",
          addIngredient: "Add Ingredient",
          preparationSteps: "Preparation Steps",
          addStep: "Add Step",
          cookingTime: "Cooking Time (minutes)",
          difficultyLevel: "Difficulty Level",
          servings: "Servings",
          tags: "Tags",
          tagsPlaceholder: "Add tags (press Enter)",
          imageUpload: "Upload Image",
          videoUpload: "Upload Video",
          submitButton: "Create Recipe Snippet",
          submitting: "Creating...",
          dragDropImage: "Drag and drop an image here or click to select",
          videoPlaceholder: "Upload a short video of your finished dish",
          successMessage: "Recipe snippet created successfully!",
          errorMessage: "Failed to create recipe snippet. Please try again."
        },
        grocery: {
          title: "Find Local Ingredients",
          subtitle: "Search for ingredients at nearby grocery stores and get pricing information",
          searchTitle: "Search Ingredients",
          postalCode: "Your Postal Code",
          postalCodePlaceholder: "Enter your postal code",
          ingredientsLabel: "Ingredients",
          ingredientPlaceholder: "e.g., tomatoes, cheese, basil",
          addIngredient: "Add Ingredient",
          searchButton: "🔍 Search Stores",
          searching: "Searching...",
          distance: "Maximum Distance",
          budget: "Budget Preference",
          delivery: "Delivery Preference",
          noResults: "No grocery stores found in your area",
          storeResults: "stores found within",
          miles: "miles"
        },
        quickeats: {
          title: "Lambalia Quick Eats Training",
          sections: {
            introduction: "Your Quick Service Advantage",
            competition: "Fast Food Competition", 
            advantages: "Why You Win",
            efficiency: "Speed & Quality",
            offerings: "Perfect Menu Items",
            operations: "Seamless Operations",
            success: "Building Success"
          },
          welcomeTitle: "Welcome, Quick Eats Provider!",
          welcomeSubtitle: "You're bringing authentic home flavors to the fast casual world. Your mission: deliver quality, culture, and care at the speed modern life demands.",
          uniquePosition: "Your Unique Position",
          whatYouProvide: "What You Provide:",
          whatFastFoodOffers: "What Fast Food Offers:"
        }
      },

      // Restaurant
      restaurant: {
        marketplace: {
          title: "Restaurant Marketplace",
          subtitle: "Discover home kitchens and traditional restaurants offering unique culinary experiences",
          browseRestaurants: "Browse Restaurants",
          becomePartner: "Become Partner",
          chooseRestaurantType: "Choose your restaurant type and start earning with Lambalia",
          homeRestaurants: "Home Restaurants",
          traditionalRestaurants: "Traditional Restaurants",
          intimateDining: "Intimate dining in local homes",
          specialOrders: "Special orders and custom meals",
          available: "available",
          specialOrdersCount: "special orders",
          noHomeRestaurants: "No home restaurants available yet.",
          specialOrdersTitle: "Special Orders from Traditional Restaurants"
        },
        homeApplication: {
          title: "Home Restaurant Application",
          homeRestaurantOption: "Home Restaurant",
          traditionalRestaurantOption: "Traditional Restaurant",
          homeFeatures: {
            feature1: "Host 2-8 guests in your dining room",
            feature2: "Share authentic home-cooked meals", 
            feature3: "Flexible scheduling",
            feature4: "$30-80 per person"
          },
          traditionalFeatures: {
            feature1: "Create special order proposals",
            feature2: "Showcase signature dishes",
            feature3: "Delivery & pickup options",
            feature4: "$50-200 per person"
          },
          monthlyPotentialHome: "Monthly potential: $500-2000+",
          monthlyPotentialTraditional: "Additional revenue stream",
          personalInfo: "Personal Information",
          legalName: "Legal Name",
          phoneNumber: "Phone Number",
          homeAddress: "Home Address",
          city: "City",
          state: "State",
          postalCode: "Postal Code",
          country: "Country",
          kitchenDescription: "Kitchen Description",
          kitchenDescriptionPlaceholder: "Describe your kitchen, equipment and cooking space",
          diningCapacity: "Dining Capacity",
          cuisineSpecialties: "Cuisine Specialties",
          cuisineSpecialtiesPlaceholder: "e.g., Italian, Mexican, Vegan",
          dietaryAccommodations: "Dietary Accommodations",
          dietaryAccommodationsPlaceholder: "e.g., Gluten-free, Kosher, Halal",
          foodHandlingExperience: "Do you have food handling experience?",
          yearsCookingExperience: "Years of Cooking Experience",
          liabilityInsurance: "Do you have liability insurance?",
          emergencyContactName: "Emergency Contact Name",
          emergencyContactPhone: "Emergency Contact Phone",
          submitButton: "Submit Application",
          submitting: "Submitting Application...",
          successMessage: "Application submitted successfully! We'll review it within 3-5 business days.",
          errorMessage: "Failed to submit application. Please try again."
        },
        traditionalApplication: {
          title: "Traditional Restaurant Application",
          restaurantName: "Restaurant Name",
          businessLicenseNumber: "Business License Number",
          yearsInBusiness: "Years in Business",
          successMessage: "Restaurant application submitted successfully! We'll review it within 5-7 business days."
        }
      },

      // Eats
      eats: {
        title: "🍽️ Lambalia Eats",
        subtitle: "Real-Time Food Marketplace",
        tabs: {
          browse: "🛒 Browse Food",
          request: "🍽️ Request Food",
          offer: "👩‍🍳 Offer Food", 
          orders: "📋 My Orders",
          requests: "📤 Active Requests"
        },
        browse: {
          title: "🍳 Available Food Near You",
          refresh: "Refresh",
          noOffers: "No food offers nearby",
          noOffersMessage: "Be the first to post a delicious meal!",
          findingFood: "Finding delicious food near you..."
        },
        request: {
          title: "Request Food",
          requestType: "Request Type",
          cuisineType: "Cuisine Type",
          budget: "Budget Range",
          servings: "Number of Servings",
          deliveryTime: "Preferred Delivery Time",
          specialRequests: "Special Requests",
          submitRequest: "Submit Request"
        },
        offer: {
          title: "Offer Food",
          dishName: "Dish Name",
          description: "Description",
          price: "Price per Serving",
          availableServings: "Available Servings",
          pickupTime: "Available Pickup Time",
          deliveryOption: "Delivery Available",
          submitOffer: "Create Offer"
        }
      },

      // Charity
      charity: {
        title: "🤝❤️ Give Back - Community Impact Program",
        subtitle: "Transform your cooking into community support and earn premium benefits",
        overview: {
          title: "Community Impact Through Food",
          description: "Join our community program where your culinary skills help feed those in need while earning premium platform benefits.",
          impactStats: "Community Impact Statistics",
          totalMeals: "Total Meals Provided",
          activeVolunteers: "Active Volunteers",
          partneredOrganizations: "Partner Organizations",
          volunteersHours: "Volunteer Hours This Month"
        },
        tiers: {
          communityHelper: {
            title: "Community Helper",
            price: "Free",
            commission: "15% Commission Rate",
            requirements: "Requirements:",
            req1: "4 hours monthly volunteering",
            req2: "2 charity activities", 
            req3: "10 lbs food donated monthly"
          },
          gardenSupporter: {
            title: "Garden Supporter", 
            price: "Earned through Service",
            commission: "12% Commission Rate",
            requirements: "Requirements:",
            req1: "8 hours monthly volunteering",
            req2: "4 charity activities",
            req3: "20 lbs food donated monthly"
          },
          communityChampion: {
            title: "Community Champion",
            price: "Elite Status",
            commission: "10% Commission Rate",
            requirements: "Requirements:",
            req1: "12 hours monthly volunteering",
            req2: "5 charity activities",
            req3: "30 lbs food donated monthly"
          }
        },
        benefits: {
          premiumBadge: "Premium Community Badge",
          reducedCommission: "Reduced Commission Rates",
          prioritySupport: "Priority Customer Support",
          featuredProfile: "Featured Profile Placement",
          exclusiveEvents: "Exclusive Community Events",
          advancedTools: "Advanced Marketing Tools",
          directMessaging: "Direct Customer Messaging",
          premiumPlacement: "Premium Product Placement",
          localChampion: "Local Champion Badge"
        },
        registration: {
          title: "Join Community Program",
          hoursPerMonth: "Committed Hours Per Month",
          charityTypes: "Preferred Charity Types",
          locations: "Preferred Locations",
          impactGoal: "Monthly Impact Goal",
          submitButton: "Join Program 🌱",
          submitting: "Joining Program..."
        },
        actions: {
          joinProgram: "Join Community Program 🌱",
          submitActivity: "Submit Activity",
          viewDashboard: "View Dashboard", 
          findOrganizations: "Find Organizations",
          calculateImpact: "Calculate Impact"
        },
        cta: "Start making a difference in your community today!"
      },

      // Local Marketplace
      marketplace: {
        title: "🌱🛒 Local Farm Marketplace",
        subtitle: "Connect with local farms and sustainable food producers",
        tabs: {
          browse: "Browse Products",
          sell: "Sell Products", 
          charity: "Charity Dashboard",
          impact: "Community Impact"
        },
        browse: {
          title: "Local Farm Products",
          filters: "Filters",
          vendorType: "Vendor Type",
          certifications: "Certifications",
          maxDistance: "Maximum Distance",
          seasonalProducts: "Seasonal Products",
          localFarms: "Local Farms",
          noFarms: "No local farms found in your area",
          noProducts: "No products available"
        }
      },

      // Smart Cooking
      smartCooking: {
        title: "🧠 Enhanced Smart Cooking Assistant",
        subtitle: "AI-powered recipe generation and cooking guidance",
        features: {
          recipeGeneration: "Recipe Generation",
          ingredientAnalysis: "Ingredient Analysis",
          cookingTips: "Smart Cooking Tips",
          nutritionInfo: "Nutrition Information"
        },
        ingredients: {
          addIngredient: "Add Ingredient",
          ingredientList: "Available Ingredients",
          noIngredients: "No ingredients added yet"
        },
        recipe: {
          generateRecipe: "Generate Recipe",
          generating: "Generating recipe...",
          instructions: "Cooking Instructions",
          prepTime: "Prep Time",
          cookTime: "Cook Time",
          difficulty: "Difficulty",
          servings: "Servings"
        }
      },

      // Profile
      profile: {
        title: "Profile",
        personalInfo: "Personal Information",
        preferences: "Preferences",
        settings: "Settings",
        earnings: "Earnings",
        tips: "Tips",
        withdraw: "Withdraw Earnings",
        profilePhoto: "Profile Photo",
        uploadPhoto: "Upload Photo",
        changePhoto: "Change Photo",
        removePhoto: "Remove Photo",
        location: "Location",
        dietaryPreferences: "Dietary Preferences",
        culturalBackground: "Cultural Background",
        cookingExperience: "Cooking Experience",
        specialties: "Specialties",
        languages: "Languages",
        about: "About Me",
        contactInfo: "Contact Information",
        currentEarnings: "Current Earnings",
        totalTips: "Total Tips",
        withdrawalHistory: "Withdrawal History",
        accountSettings: "Account Settings",
        notificationSettings: "Notification Settings",
        privacySettings: "Privacy Settings"
      },

      // Footer
      footer: {
        aboutUs: "About Us",
        contactUs: "Contact Us", 
        privacyPolicy: "Privacy Policy",
        termsOfService: "Terms of Service",
        careers: "Careers",
        blog: "Blog",
        support: "Support",
        community: "Community",
        store: "Store"
      },

      // Careers
      careers: {
        title: "Join Our Team",
        subtitle: "Help us build the future of cultural food sharing",
        positions: "Open Positions",
        apply: "Apply Now",
        requirements: "Requirements",
        responsibilities: "Responsibilities",
        benefits: "Benefits",
        remote: "Remote",
        fullTime: "Full-time",
        partTime: "Part-time",
        contract: "Contract"
      },

      // Contact
      contact: {
        title: "Contact Us",
        subtitle: "Get in touch with our team",
        name: "Name",
        email: "Email",
        subject: "Subject",
        message: "Message",
        send: "Send Message",
        sending: "Sending...",
        successMessage: "Message sent successfully!",
        errorMessage: "Failed to send message. Please try again."
      },

      // Cuisines
      cuisines: {
        american: "American",
        mexican: "Mexican",
        italian: "Italian", 
        chinese: "Chinese",
        indian: "Indian",
        japanese: "Japanese",
        thai: "Thai",
        mediterranean: "Mediterranean",
        african: "African",
        middleEastern: "Middle Eastern",
        caribbean: "Caribbean",
        fusion: "Fusion",
        comfortFood: "Comfort Food",
        healthy: "Healthy",
        vegan: "Vegan",
        vegetarian: "Vegetarian",
        desserts: "Desserts",
        breakfast: "Breakfast",
        lunch: "Lunch",
        dinner: "Dinner"
      }
    }
  },

  es: {
    translation: {
      nav: {
        browse: "Explorar Plantillas",
        create: "Crear Fragmento",
        ingredients: "Encontrar Ingredientes", 
        restaurant: "Abrir Cocina",
        marketplace: "Mercado Local",
        charity: "Retribuir",
        eats: "Comida Rápida",
        offers: "Ofertas Locales",
        profile: "Perfil"
      },
      
      common: {
        loading: "Cargando...",
        submit: "Enviar",
        cancel: "Cancelar",
        save: "Guardar",
        edit: "Editar",
        delete: "Eliminar",
        search: "Buscar",
        filter: "Filtrar",
        sort: "Ordenar",
        back: "Atrás",
        next: "Siguiente",
        previous: "Anterior",
        close: "Cerrar",
        open: "Abrir",
        yes: "Sí",
        no: "No",
        ok: "OK",
        error: "Error",
        success: "Éxito",
        warning: "Advertencia",
        info: "Información",
        viewMore: "Ver Más",
        readMore: "Leer Más",
        showLess: "Mostrar Menos",
        noResults: "No se encontraron resultados",
        selectOption: "Seleccionar una opción",
        pleaseWait: "Por favor espera...",
        tryAgain: "Intentar de nuevo"
      },

      auth: {
        login: "Iniciar Sesión",
        register: "Registrarse",
        logout: "Cerrar Sesión",
        email: "Correo Electrónico",
        password: "Contraseña",
        username: "Nombre de Usuario",
        fullName: "Nombre Completo",
        postalCode: "Código Postal",
        phoneNumber: "Número de Teléfono",
        forgotPassword: "¿Olvidaste tu contraseña?",
        rememberMe: "Recordarme",
        loginButton: "Entra a Tu Cocina 👨‍🍳",
        registerButton: "Unirse a la Comunidad",
        joinLambalia: "Únete a Lambalia",
        welcomeMessage: "¡Únete a nuestra comunidad de chefs caseros compartiendo recetas auténticas de todo el mundo!",
        alreadyHaveAccount: "¿Ya tienes una cuenta?",
        dontHaveAccount: "¿No tienes una cuenta?",
        createAccount: "Crear Cuenta",
        signIn: "Iniciar Sesión"
      },

      home: {
        title: "Lambalia",
        subtitle: "Saborea el Patrimonio del Mundo",
        welcomeMessage: "¡Únete a nuestra comunidad de chefs caseros compartiendo recetas auténticas de todo el mundo!",
        description: "Conecta con chefs caseros apasionados, descubre recetas auténticas y convierte tu cocina en una experiencia culinaria global.",
        getStarted: "Comenzar",
        learnMore: "Saber Más",
        features: {
          recipes: "198+ Recetas Tradicionales",
          monetize: "Monetiza Tus Habilidades Culinarias",
          restaurant: "Plataforma de Restaurante Casero",
          communities: "80+ Comunidades Culturales",
          heritageRecipes: "Recetas Patrimoniales",
          specialtyIngredients: "Ingredientes Especiales"
        },
        actions: {
          browseName: "📚 Explorar Plantillas",
          createName: "✨ Crear Fragmento",
          ingredientsName: "🛒 Encontrar Ingredientes", 
          restaurantName: "🏠👩‍🍳 Abrir Cocina",
          marketplaceName: "🌱🛒 Mercado Local",
          charityName: "🤝❤️ Retribuir",
          eatsName: "🚚🍽️ Comida Rápida",
          offersName: "🔍 Ofertas Locales"
        },
        cookingClasses: {
          title: "Clases de Cocina en Línea",
          description: "Aprende de chefs maestros de todo el mundo",
          learnMore: "Saber Más"
        },
        recipeSnippets: {
          title: "Últimos Consejos de Recetas",
          subtitle: "Consejos rápidos de cocina de nuestra comunidad",
          viewAll: "Ver Todos los Consejos",
          cookingTip: "Consejo de Cocina",
          noSnippets: "No se encontraron consejos de recetas. ¡Sé el primero en compartir tu consejo de receta tradicional en Lambalia!"
        },
        communityStats: {
          title: "Únete a Nuestra Comunidad Culinaria Global",
          activeChefs: "Chefs Caseros Activos",
          countriesServed: "Países Atendidos",
          recipesShared: "Recetas Compartidas",
          culturesRepresented: "Culturas Representadas"
        }
      },

      forms: {
        createSnippet: {
          title: "Crear Consejo de Receta",
          recipeTitle: "Título de la Receta",
          recipeTitlePlaceholder: "Ingresa el nombre de la receta",
          localTitle: "Título Local",
          localTitlePlaceholder: "Nombre de la receta en tu idioma local (opcional)",
          description: "Descripción",
          descriptionPlaceholder: "Describe tu receta",
          snippetType: "Tipo de Consejo",
          ingredients: "Ingredientes",
          ingredientName: "Ingrediente",
          amount: "Cantidad",
          unit: "Unidad",
          addIngredient: "Agregar Ingrediente",
          preparationSteps: "Pasos de Preparación",
          addStep: "Agregar Paso",
          cookingTime: "Tiempo de Cocción (minutos)",
          difficultyLevel: "Nivel de Dificultad",
          servings: "Porciones",
          tags: "Etiquetas",
          tagsPlaceholder: "Agregar etiquetas (presiona Enter)",
          imageUpload: "Subir Imagen",
          videoUpload: "Subir Video",
          submitButton: "Crear Consejo de Receta",
          submitting: "Creando...",
          dragDropImage: "Arrastra y suelta una imagen aquí o haz clic para seleccionar",
          videoPlaceholder: "Sube un video corto de tu platillo terminado",
          successMessage: "¡Consejo de receta creado exitosamente!",
          errorMessage: "Error al crear el consejo de receta. Por favor, inténtalo de nuevo."
        },
        grocery: {
          title: "Encontrar Ingredientes Locales",
          subtitle: "Busca ingredientes en tiendas cercanas y obtén información de precios",
          searchTitle: "Buscar Ingredientes",
          postalCode: "Tu Código Postal",
          postalCodePlaceholder: "Ingresa tu código postal",
          ingredientsLabel: "Ingredientes",
          ingredientPlaceholder: "ej., tomates, queso, albahaca",
          addIngredient: "Agregar Ingrediente",
          searchButton: "🔍 Buscar Tiendas",
          searching: "Buscando...",
          distance: "Distancia Máxima",
          budget: "Preferencia de Presupuesto",
          delivery: "Preferencia de Entrega",
          noResults: "No se encontraron tiendas en tu área",
          storeResults: "tiendas encontradas dentro de",
          miles: "millas"
        }
      },

      restaurant: {
        marketplace: {
          title: "Mercado de Restaurantes",
          subtitle: "Descubre cocinas caseras y restaurantes tradicionales que ofrecen experiencias culinarias únicas",
          browseRestaurants: "Explorar Restaurantes",
          becomePartner: "Convertirse en Socio",
          chooseRestaurantType: "Elige tu tipo de restaurante y comienza a ganar con Lambalia",
          homeRestaurants: "Restaurantes Caseros",
          traditionalRestaurants: "Restaurantes Tradicionales",
          intimateDining: "Comidas íntimas en hogares locales",
          specialOrders: "Pedidos especiales y comidas personalizadas",
          available: "disponible",
          specialOrdersCount: "pedidos especiales",
          noHomeRestaurants: "No hay restaurantes caseros disponibles aún.",
          specialOrdersTitle: "Pedidos Especiales de Restaurantes Tradicionales"
        },
        homeApplication: {
          title: "Solicitud de Restaurante Casero",
          homeRestaurantOption: "Restaurante Casero",
          traditionalRestaurantOption: "Restaurante Tradicional",
          homeFeatures: {
            feature1: "Aloja 2-8 invitados en tu comedor",
            feature2: "Comparte comidas auténticas caseras", 
            feature3: "Horarios flexibles",
            feature4: "$30-80 por persona"
          },
          traditionalFeatures: {
            feature1: "Crea propuestas de pedidos especiales",
            feature2: "Muestra tus platos distintivos",
            feature3: "Opciones de entrega y recogida",
            feature4: "$50-200 por persona"
          },
          monthlyPotentialHome: "Potencial mensual: $500-2000+",
          monthlyPotentialTraditional: "Fuente de ingresos adicional",
          personalInfo: "Información Personal",
          legalName: "Nombre Legal",
          phoneNumber: "Número de Teléfono",
          homeAddress: "Dirección del Domicilio",
          city: "Ciudad",
          state: "Estado",
          postalCode: "Código Postal",
          country: "País",
          kitchenDescription: "Descripción de la Cocina",
          kitchenDescriptionPlaceholder: "Describe tu cocina, equipos y espacio de cocción",
          diningCapacity: "Capacidad del Comedor",
          cuisineSpecialties: "Especialidades Culinarias",
          cuisineSpecialtiesPlaceholder: "ej., Italiana, Mexicana, Vegana",
          dietaryAccommodations: "Adaptaciones Dietéticas",
          dietaryAccommodationsPlaceholder: "ej., Sin gluten, Kosher, Halal",
          foodHandlingExperience: "¿Tienes experiencia en manipulación de alimentos?",
          yearsCookingExperience: "Años de Experiencia Cocinando",
          liabilityInsurance: "¿Tienes seguro de responsabilidad civil?",
          emergencyContactName: "Nombre de Contacto de Emergencia",
          emergencyContactPhone: "Teléfono de Contacto de Emergencia",
          submitButton: "Enviar Solicitud",
          submitting: "Enviando Solicitud...",
          successMessage: "¡Solicitud enviada exitosamente! La revisaremos en 3-5 días hábiles.",
          errorMessage: "Error al enviar la solicitud. Por favor, inténtalo de nuevo."
        }
      },

      charity: {
        title: "🤝❤️ Retribuir - Programa de Impacto Comunitario",
        subtitle: "Transforma tu cocina en apoyo comunitario y gana beneficios premium",
        actions: {
          joinProgram: "Únete al Programa Comunitario 🌱"
        },
        cta: "¡Comienza a hacer la diferencia en tu comunidad hoy!"
      },

      cuisines: {
        american: "Americana",
        mexican: "Mexicana",
        italian: "Italiana", 
        chinese: "China",
        indian: "India",
        japanese: "Japonesa",
        thai: "Tailandesa",
        mediterranean: "Mediterránea",
        african: "Africana",
        middleEastern: "Medio Oriente",
        caribbean: "Caribeña",
        fusion: "Fusión",
        comfortFood: "Comida Reconfortante",
        healthy: "Saludable",
        vegan: "Vegana",
        vegetarian: "Vegetariana",
        desserts: "Postres"
      }
    }
  },

  fr: {
    translation: {
      nav: {
        browse: "Parcourir Modèles",
        create: "Créer Extrait",
        ingredients: "Trouver Ingrédients",
        restaurant: "Ouvrir Cuisine", 
        marketplace: "Marché Local",
        charity: "Donner en Retour",
        eats: "Repas Rapides",
        offers: "Offres Locales",
        profile: "Profil"
      },

      // Browse Templates
      browseTemplates: {
        title: "Modèles de Recettes Traditionnelles",
        subtitle: "Choisissez parmi {count} pays avec des centaines de recettes authentiques",
        searchPlaceholder: "Rechercher recettes ou ingrédients...",
        allCountries: "Tous les Pays (80+)",
        keyIngredients: "Ingrédients Clés:",
        culturalNote: "Note Culturelle:",
        featured: "En Vedette",
        useTemplate: "Utiliser ce Modèle",
        difficulty: "Difficulté",
        estimatedTime: "Temps Estimé",
        servingSize: "Taille de Portion",
        recipes: "recettes",
        moreIngredients: "de plus"
      },
      
      common: {
        loading: "Chargement...",
        submit: "Soumettre",
        cancel: "Annuler",
        save: "Sauvegarder",
        edit: "Modifier",
        delete: "Supprimer",
        search: "Rechercher",
        filter: "Filtrer",
        sort: "Trier",
        back: "Retour",
        next: "Suivant",
        previous: "Précédent",
        close: "Fermer",
        open: "Ouvrir",
        yes: "Oui",
        no: "Non",
        ok: "OK",
        error: "Erreur",
        success: "Succès",
        warning: "Avertissement",
        info: "Information",
        viewMore: "Voir Plus",
        readMore: "Lire Plus",
        showLess: "Afficher Moins",
        noResults: "Aucun résultat trouvé",
        selectOption: "Sélectionner une option",
        pleaseWait: "Veuillez patienter...",
        tryAgain: "Réessayer"
      },

      auth: {
        login: "Connexion",
        register: "S'inscrire",
        logout: "Déconnexion",
        email: "Email",
        password: "Mot de passe",
        username: "Nom d'utilisateur",
        fullName: "Nom complet",
        postalCode: "Code postal",
        phoneNumber: "Numéro de téléphone",
        forgotPassword: "Mot de passe oublié?",
        rememberMe: "Se souvenir de moi",
        loginButton: "Entrez dans Votre Cuisine 👨‍🍳",
        registerButton: "Rejoindre la Communauté",
        joinLambalia: "Rejoindre Lambalia",
        welcomeMessage: "Rejoignez notre communauté de chefs à domicile partageant des recettes authentiques du monde entier!",
        alreadyHaveAccount: "Vous avez déjà un compte?",
        dontHaveAccount: "Vous n'avez pas de compte?",
        createAccount: "Créer un Compte",
        signIn: "Se Connecter"
      },

      home: {
        title: "Lambalia", 
        subtitle: "Goûtez au Patrimoine du Monde",
        welcomeMessage: "Rejoignez notre communauté de chefs à domicile partageant des recettes authentiques du monde entier !",
        description: "Connectez-vous avec des chefs passionnés, découvrez des recettes authentiques et transformez votre cuisine en une expérience culinaire mondiale.",
        getStarted: "Commencer",
        learnMore: "En Savoir Plus"
      },

      restaurant: {
        marketplace: {
          title: "Marché des Restaurants",
          subtitle: "Découvrez des cuisines maison et des restaurants traditionnels offrant des expériences culinaires uniques",
          browseRestaurants: "Parcourir Restaurants",
          becomePartner: "Devenir Partenaire",
          chooseRestaurantType: "Choisissez votre type de restaurant et commencez à gagner avec Lambalia",
          homeRestaurants: "Restaurants à Domicile",
          traditionalRestaurants: "Restaurants Traditionnels"
        },
        homeApplication: {
          title: "Candidature Restaurant à Domicile",
          homeRestaurantOption: "Restaurant à Domicile",
          traditionalRestaurantOption: "Restaurant Traditionnel",
          homeFeatures: {
            feature1: "Accueillez 2-8 invités dans votre salle à manger",
            feature2: "Partagez des repas authentiques faits maison", 
            feature3: "Horaires flexibles",
            feature4: "30-80€ par personne"
          },
          traditionalFeatures: {
            feature1: "Créez des propositions de commandes spéciales",
            feature2: "Présentez vos plats signature",
            feature3: "Options de livraison et de retrait",
            feature4: "50-200€ par personne"
          },
          monthlyPotentialHome: "Potentiel mensuel: 500-2000€+",
          monthlyPotentialTraditional: "Source de revenus supplémentaire",
          legalName: "Nom Légal",
          phoneNumber: "Numéro de Téléphone"
        }
      },

      charity: {
        title: "🤝❤️ Donner en Retour - Programme d'Impact Communautaire",
        subtitle: "Transformez votre cuisine en soutien communautaire et gagnez des avantages premium",
        actions: {
          joinProgram: "Rejoindre le Programme Communautaire 🌱"
        },
        cta: "Commencez à faire la différence dans votre communauté dès aujourd'hui!"
      },

      cuisines: {
        american: "Américaine",
        mexican: "Mexicaine",
        italian: "Italienne", 
        chinese: "Chinoise",
        indian: "Indienne",
        japanese: "Japonaise",
        thai: "Thaïlandaise",
        mediterranean: "Méditerranéenne",
        african: "Africaine",
        middleEastern: "Moyen-Orient",
        caribbean: "Caribéenne",
        fusion: "Fusion"
      }
    }
  },

  de: {
    translation: {
      nav: {
        browse: "Vorlagen Durchsuchen",
        create: "Snippet Erstellen", 
        ingredients: "Zutaten Finden",
        restaurant: "Küche Öffnen",
        marketplace: "Lokaler Markt",
        charity: "Zurückgeben",
        eats: "Schnelles Essen",
        offers: "Lokale Angebote",
        profile: "Profil"
      },

      common: {
        loading: "Lädt...",
        submit: "Absenden",
        cancel: "Abbrechen",
        save: "Speichern",
        edit: "Bearbeiten",
        delete: "Löschen",
        search: "Suchen"
      },

      auth: {
        login: "Anmelden",
        register: "Registrieren",
        logout: "Abmelden",
        email: "E-Mail",
        password: "Passwort",
        username: "Benutzername",
        fullName: "Vollständiger Name",
        postalCode: "Postleitzahl",
        phoneNumber: "Telefonnummer",
        loginButton: "Betreten Sie Ihre Küche 👨‍🍳",
        registerButton: "Der Gemeinschaft Beitreten",
        joinLambalia: "Lambalia Beitreten"
      },

      home: {
        title: "Lambalia",
        subtitle: "Schmecken Sie das Erbe der Welt"
      },

      restaurant: {
        marketplace: {
          title: "Restaurant-Marktplatz",
          becomePartner: "Partner Werden",
          homeRestaurants: "Heimrestaurants"
        }
      },

      cuisines: {
        american: "Amerikanisch",
        mexican: "Mexikanisch", 
        italian: "Italienisch",
        chinese: "Chinesisch",
        indian: "Indisch",
        japanese: "Japanisch",
        thai: "Thailändisch",
        mediterranean: "Mediterran",
        german: "Deutsch"
      }
    }
  },

  pt: {
    translation: {
      nav: {
        browse: "Navegar Modelos",
        create: "Criar Trecho",
        ingredients: "Encontrar Ingredientes",
        restaurant: "Abrir Cozinha",
        marketplace: "Mercado Local",
        charity: "Retribuir", 
        eats: "Comida Rápida",
        profile: "Perfil"
      },

      auth: {
        login: "Entrar",
        register: "Registrar",
        logout: "Sair",
        email: "Email",
        password: "Senha",
        username: "Nome de usuário",
        fullName: "Nome completo",
        postalCode: "CEP",
        phoneNumber: "Número de telefone",
        loginButton: "Entre na Sua Cozinha 👨‍🍳",
        registerButton: "Juntar-se à Comunidade",
        joinLambalia: "Junte-se ao Lambalia"
      },

      restaurant: {
        marketplace: {
          title: "Mercado de Restaurantes",
          becomePartner: "Tornar-se Parceiro",
          homeRestaurants: "Restaurantes Caseiros"
        },
        homeApplication: {
          title: "Candidatura Restaurante Domiciliar",
          legalName: "Nome Legal",
          phoneNumber: "Número de Telefone"
        }
      },

      cuisines: {
        american: "Americana",
        mexican: "Mexicana",
        italian: "Italiana",
        chinese: "Chinesa",
        portuguese: "Portuguesa"
      }
    }
  },

  ru: {
    translation: {
      nav: {
        browse: "Просмотр Шаблонов",
        create: "Создать Фрагмент",
        ingredients: "Найти Ингредиенты",
        restaurant: "Открыть Кухню",
        marketplace: "Местный Рынок",
        charity: "Благотворительность",
        eats: "Быстрое Питание",
        profile: "Профиль"
      },

      auth: {
        login: "Войти",
        register: "Регистрация", 
        logout: "Выйти",
        email: "Электронная почта",
        password: "Пароль",
        username: "Имя пользователя",
        fullName: "Полное имя",
        postalCode: "Почтовый индекс",
        phoneNumber: "Номер телефона",
        loginButton: "Войдите в Вашу Кухню 👨‍🍳",
        registerButton: "Присоединиться к Сообществу",
        joinLambalia: "Присоединиться к Lambalia"
      },

      restaurant: {
        marketplace: {
          title: "Рынок Ресторанов",
          becomePartner: "Стать Партнером",
          homeRestaurants: "Домашние Рестораны"
        },
        homeApplication: {
          title: "Заявка на Домашний Ресторан",
          legalName: "Юридическое Имя",
          phoneNumber: "Номер Телефона"
        }
      },

      cuisines: {
        american: "Американская",
        russian: "Русская"
      }
    }
  },

  it: {
    translation: {
      nav: {
        browse: "Sfoglia Modelli",
        create: "Crea Frammento",
        ingredients: "Trova Ingredienti",
        restaurant: "Apri Cucina",
        marketplace: "Mercato Locale",
        charity: "Dare Indietro",
        eats: "Cibo Veloce",
        profile: "Profilo"
      },

      auth: {
        login: "Accedi",
        register: "Registrati",
        logout: "Disconnetti",
        email: "Email",
        password: "Password", 
        username: "Nome utente",
        fullName: "Nome completo",
        postalCode: "Codice postale",
        phoneNumber: "Numero di telefono",
        loginButton: "Entra nella Tua Cucina 👨‍🍳",
        registerButton: "Unisciti alla Comunità",
        joinLambalia: "Unisciti a Lambalia"
      },

      restaurant: {
        marketplace: {
          title: "Mercato Ristoranti",
          becomePartner: "Diventa Partner",
          homeRestaurants: "Ristoranti Casalinghi"
        },
        homeApplication: {
          title: "Candidatura Ristorante Domestico",
          legalName: "Nome Legale",
          phoneNumber: "Numero di Telefono"
        }
      },

      cuisines: {
        american: "Americana",
        italian: "Italiana"
      }
    }
  },

  ar: {
    translation: {
      nav: {
        browse: "تصفح القوالب",
        create: "إنشاء مقطع",
        ingredients: "البحث عن المكونات", 
        restaurant: "فتح المطبخ",
        marketplace: "السوق المحلي",
        charity: "العطاء",
        eats: "الطعام السريع",
        offers: "العروض المحلية",
        profile: "الملف الشخصي"
      },
      
      auth: {
        login: "تسجيل الدخول",
        register: "التسجيل",
        logout: "تسجيل الخروج",
        email: "البريد الإلكتروني",
        password: "كلمة المرور",
        username: "اسم المستخدم",
        fullName: "الاسم الكامل",
        postalCode: "الرمز البريدي",
        phoneNumber: "رقم الهاتف",
        loginButton: "ادخل إلى مطبخك 👨‍🍳",
        registerButton: "انضم للمجتمع",
        joinLambalia: "انضم إلى لامباليا"
      },

      restaurant: {
        marketplace: {
          title: "سوق المطاعم",
          becomePartner: "كن شريكاً",
          homeRestaurants: "المطاعم المنزلية"
        },
        homeApplication: {
          title: "طلب مطعم منزلي",
          legalName: "الاسم القانوني",
          phoneNumber: "رقم الهاتف"
        }
      },

      cuisines: {
        american: "أمريكية",
        middleEastern: "شرق أوسطية"
      }
    }
  },

  hi: {
    translation: {
      nav: {
        browse: "टेम्प्लेट ब्राउज़ करें",
        create: "स्निपेट बनाएं",
        ingredients: "सामग्री खोजें",
        restaurant: "रसोई खोलें",
        marketplace: "स्थानीय बाजार",
        charity: "वापस दें",
        eats: "तुरंत खाना",
        offers: "स्थानीय ऑफर",
        profile: "प्रोफ़ाइल"
      },

      auth: {
        login: "लॉग इन करें",
        register: "रजिस्टर करें",
        logout: "लॉग आउट",
        email: "ईमेल",
        password: "पासवर्ड",
        username: "उपयोगकर्ता नाम",
        fullName: "पूरा नाम",
        postalCode: "पिन कोड",
        phoneNumber: "फोन नंबर",
        loginButton: "अपनी रसोई में प्रवेश करें 👨‍🍳",
        registerButton: "समुदाय में शामिल हों",
        joinLambalia: "लैम्बालिया में शामिल हों"
      },

      restaurant: {
        marketplace: {
          title: "रेस्टोरेंट बाजार",
          becomePartner: "साझीदार बनें",
          homeRestaurants: "होम रेस्टोरेंट"
        },
        homeApplication: {
          title: "होम रेस्टोरेंट आवेदन",
          legalName: "कानूनी नाम",
          phoneNumber: "फोन नंबर"
        }
      },

      cuisines: {
        american: "अमेरिकी",
        indian: "भारतीय"
      }
    }
  }
};

i18n
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    resources,
    fallbackLng: 'en',
    debug: false,

    interpolation: {
      escapeValue: false, // React already does escaping
    },

    detection: {
      order: ['localStorage', 'sessionStorage', 'navigator', 'htmlTag'],
      caches: ['localStorage', 'sessionStorage'],
    }
  });

export default i18n;