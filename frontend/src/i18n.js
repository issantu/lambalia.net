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
        info: "Information"
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
        welcomeMessage: "Join our community of home chefs sharing authentic recipes from around the world!"
      },

      // Home
      home: {
        title: "Lambalia",
        subtitle: "Taste the World's Heritage",
        welcomeMessage: "Join our community of home chefs sharing authentic recipes from around the world!",
        description: "Connect with passionate home chefs, discover authentic recipes, and turn your kitchen into a global culinary experience.",
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
          eatsName: "🚚🍽️ Quick Eats"
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
          videoPlaceholder: "Upload a short video of your finished dish"
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
          delivery: "Delivery Preference"
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
        desserts: "Desserts"
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
        info: "Información"
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
        welcomeMessage: "¡Únete a nuestra comunidad de chefs caseros compartiendo recetas auténticas de todo el mundo!"
      },

      home: {
        title: "Lambalia",
        subtitle: "Saborea el Patrimonio del Mundo",
        welcomeMessage: "¡Únete a nuestra comunidad de chefs caseros compartiendo recetas auténticas de todo el mundo!",
        description: "Conecta con chefs caseros apasionados, descubre recetas auténticas y convierte tu cocina en una experiencia culinaria global.",
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
          eatsName: "🚚🍽️ Comida Rápida"
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

      // Forms
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
          videoPlaceholder: "Sube un video corto de tu platillo terminado"
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
          delivery: "Preferencia de Entrega"
        },
        quickeats: {
          title: "Entrenamiento Lambalia Comida Rápida",
          sections: {
            introduction: "Tu Ventaja de Servicio Rápido",
            competition: "Competencia de Comida Rápida", 
            advantages: "Por Qué Ganas Tú",
            efficiency: "Velocidad y Calidad",
            offerings: "Elementos de Menú Perfectos",
            operations: "Operaciones Sin Problemas",
            success: "Construyendo el Éxito"
          },
          welcomeTitle: "¡Bienvenido, Proveedor de Comida Rápida!",
          welcomeSubtitle: "Estás trayendo sabores auténticos caseros al mundo de la comida casual rápida. Tu misión: entregar calidad, cultura y cuidado a la velocidad que la vida moderna demanda.",
          uniquePosition: "Tu Posición Única",
          whatYouProvide: "Lo Que Tú Proporcionas:",
          whatFastFoodOffers: "Lo Que Ofrece la Comida Rápida:"
        }
      },

      restaurant: {
        marketplace: {
          title: "Mercado de Restaurantes",
          subtitle: "Descubre cocinas caseras y restaurantes tradicionales que ofrecen experiencias culinarias únicas",
          browseRestaurants: "Explorar Restaurantes",
          becomePartner: "Convertirse en Socio",
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
        },
        traditionalApplication: {
          title: "Solicitud de Restaurante Tradicional",
          restaurantName: "Nombre del Restaurante",
          businessLicenseNumber: "Número de Licencia Comercial",
          yearsInBusiness: "Años en el Negocio",
          successMessage: "¡Solicitud de restaurante enviada exitosamente! La revisaremos en 5-7 días hábiles."
        }
      },

      eats: {
        title: "🍽️ Lambalia Eats",
        subtitle: "Mercado de Comida en Tiempo Real",
        tabs: {
          browse: "🛒 Explorar Comida",
          request: "🍽️ Solicitar Comida",
          offer: "👩‍🍳 Ofrecer Comida", 
          orders: "📋 Mis Pedidos",
          requests: "📤 Solicitudes Activas"
        },
        browse: {
          title: "🍳 Comida Disponible Cerca de Ti",
          refresh: "Actualizar",
          noOffers: "No hay ofertas de comida cerca",
          noOffersMessage: "¡Sé el primero en publicar una comida deliciosa!",
          findingFood: "Encontrando comida deliciosa cerca de ti..."
        }
      },

      charity: {
        title: "🤝❤️ Retribuir - Programa de Impacto Comunitario",
        subtitle: "Transforma tu cocina en apoyo comunitario y gana beneficios premium",
        overview: {
          title: "Impacto Comunitario a Través de la Comida",
          description: "Únete a nuestro programa comunitario donde tus habilidades culinarias ayudan a alimentar a quienes lo necesitan mientras obtienes beneficios premium en la plataforma.",
          impactStats: "Estadísticas de Impacto Comunitario",
          totalMeals: "Total de Comidas Proporcionadas",
          activeVolunteers: "Voluntarios Activos",
          partneredOrganizations: "Organizaciones Asociadas",
          volunteersHours: "Horas de Voluntariado Este Mes"
        },
        tiers: {
          communityHelper: {
            title: "Ayudante Comunitario",
            price: "Gratis",
            commission: "Tasa de Comisión 15%",
            requirements: "Requisitos:",
            req1: "4 horas mensuales de voluntariado",
            req2: "2 actividades benéficas", 
            req3: "10 libras de comida donada mensualmente"
          },
          gardenSupporter: {
            title: "Partidario del Jardín", 
            price: "Ganado a Través del Servicio",
            commission: "Tasa de Comisión 12%",
            requirements: "Requisitos:",
            req1: "8 horas mensuales de voluntariado",
            req2: "4 actividades benéficas",
            req3: "20 libras de comida donada mensualmente"
          },
          communityChampion: {
            title: "Campeón Comunitario",
            price: "Estado Elite",
            commission: "Tasa de Comisión 10%",
            requirements: "Requisitos:",
            req1: "12 horas mensuales de voluntariado",
            req2: "5 actividades benéficas",
            req3: "30 libras de comida donada mensualmente"
          }
        },
        benefits: {
          premiumBadge: "Insignia Premium Comunitaria",
          reducedCommission: "Tasas de Comisión Reducidas",
          prioritySupport: "Soporte Prioritario al Cliente",
          featuredProfile: "Colocación de Perfil Destacado",
          exclusiveEvents: "Eventos Comunitarios Exclusivos",
          advancedTools: "Herramientas de Marketing Avanzadas",
          directMessaging: "Mensajería Directa al Cliente",
          premiumPlacement: "Colocación Premium de Producto",
          localChampion: "Insignia de Campeón Local"
        },
        registration: {
          title: "Únete al Programa Comunitario",
          hoursPerMonth: "Horas Comprometidas Por Mes",
          charityTypes: "Tipos de Caridad Preferidos",
          locations: "Ubicaciones Preferidas",
          impactGoal: "Meta de Impacto Mensual",
          submitButton: "Unirse al Programa 🌱",
          submitting: "Uniéndose al Programa..."
        },
        actions: {
          joinProgram: "Únete al Programa Comunitario 🌱",
          submitActivity: "Enviar Actividad",
          viewDashboard: "Ver Panel", 
          findOrganizations: "Encontrar Organizaciones",
          calculateImpact: "Calcular Impacto"
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
        info: "Information"
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
        forgotPassword: "Mot de passe oublié?",
        rememberMe: "Se souvenir de moi",
        loginButton: "Entrez dans Votre Cuisine 👨‍🍳",
        registerButton: "Rejoindre la Communauté",
        joinLambalia: "Rejoindre Lambalia",
        welcomeMessage: "Rejoignez notre communauté de chefs à domicile partageant des recettes authentiques du monde entier!"
      },

      home: {
        title: "Lambalia", 
        subtitle: "Goûtez au Patrimoine du Monde",
        welcomeMessage: "Rejoignez notre communauté de chefs à domicile partageant des recettes authentiques du monde entier !",
        description: "Connectez-vous avec des chefs passionnés, découvrez des recettes authentiques et transformez votre cuisine en une expérience culinaire mondiale.",
        features: {
          recipes: "198+ Recettes Traditionnelles",
          monetize: "Monétisez Votre Cuisine",
          restaurant: "Plateforme de Restaurant à Domicile",
          communities: "80+ Communautés Culturelles",
          heritageRecipes: "Recettes Patrimoniales",
          specialtyIngredients: "Ingrédients Spéciaux"
        },
        actions: {
          browseName: "📚 Parcourir Modèles",
          createName: "✨ Créer Extrait",
          ingredientsName: "🛒 Trouver Ingrédients", 
          restaurantName: "🏠👩‍🍳 Ouvrir Cuisine",
          marketplaceName: "🌱🛒 Marché Local",
          charityName: "🤝❤️ Donner en Retour",
          eatsName: "🚚🍽️ Repas Rapides"
        },
        cookingClasses: {
          title: "Cours de Cuisine en Ligne",
          description: "Apprenez des chefs maîtres du monde entier",
          learnMore: "En Savoir Plus"
        },
        recipeSnippets: {
          title: "Dernières Recettes Rapides", 
          subtitle: "Conseils de cuisine rapides de notre communauté",
          viewAll: "Voir Tous les Extraits",
          cookingTip: "Conseil de Cuisine",
          noSnippets: "Aucune recette rapide trouvée. Soyez le premier à partager votre recette traditionnelle sur Lambalia !"
        },
        communityStats: {
          title: "Rejoignez Notre Communauté Culinaire Mondiale",
          activeChefs: "Chefs à Domicile Actifs",
          countriesServed: "Pays Servis",
          recipesShared: "Recettes Partagées",
          culturesRepresented: "Cultures Représentées"
        }
      },

      // Forms
      forms: {
        createSnippet: {
          title: "Créer Extrait de Recette",
          recipeTitle: "Titre de la Recette",
          recipeTitlePlaceholder: "Entrez le nom de la recette",
          localTitle: "Titre Local",
          localTitlePlaceholder: "Nom de la recette dans votre langue locale (optionnel)",
          description: "Description",
          descriptionPlaceholder: "Décrivez votre recette",
          snippetType: "Type d'Extrait",
          ingredients: "Ingrédients",
          ingredientName: "Ingrédient",
          amount: "Quantité",
          unit: "Unité",
          addIngredient: "Ajouter Ingrédient",
          preparationSteps: "Étapes de Préparation",
          addStep: "Ajouter Étape",
          cookingTime: "Temps de Cuisson (minutes)",
          difficultyLevel: "Niveau de Difficulté",
          servings: "Portions",
          tags: "Étiquettes",
          tagsPlaceholder: "Ajouter étiquettes (appuyez sur Entrée)",
          imageUpload: "Télécharger Image",
          videoUpload: "Télécharger Vidéo",
          submitButton: "Créer Extrait de Recette",
          submitting: "Création...",
          dragDropImage: "Glissez et déposez une image ici ou cliquez pour sélectionner",
          videoPlaceholder: "Téléchargez une courte vidéo de votre plat fini"
        },
        grocery: {
          title: "Trouver Ingrédients Locaux",
          subtitle: "Recherchez des ingrédients dans les magasins à proximité et obtenez des informations sur les prix",
          searchTitle: "Rechercher Ingrédients",
          postalCode: "Votre Code Postal",
          postalCodePlaceholder: "Entrez votre code postal",
          ingredientsLabel: "Ingrédients",
          ingredientPlaceholder: "ex., tomates, fromage, basilic",
          addIngredient: "Ajouter Ingrédient",
          searchButton: "🔍 Rechercher Magasins",
          searching: "Recherche...",
          distance: "Distance Maximale",
          budget: "Préférence de Budget",
          delivery: "Préférence de Livraison"
        },
        quickeats: {
          title: "Formation Lambalia Repas Rapides",
          sections: {
            introduction: "Votre Avantage Service Rapide",
            competition: "Concurrence Restauration Rapide", 
            advantages: "Pourquoi Vous Gagnez",
            efficiency: "Vitesse et Qualité",
            offerings: "Articles de Menu Parfaits",
            operations: "Opérations Fluides",
            success: "Construire le Succès"
          },
          welcomeTitle: "Bienvenue, Fournisseur de Repas Rapides!",
          welcomeSubtitle: "Vous apportez des saveurs authentiques maison au monde de la restauration rapide. Votre mission: livrer qualité, culture et soin à la vitesse que la vie moderne exige.",
          uniquePosition: "Votre Position Unique",
          whatYouProvide: "Ce Que Vous Fournissez:",
          whatFastFoodOffers: "Ce Que Offre la Restauration Rapide:"
        }
      },

      restaurant: {
        marketplace: {
          title: "Marché des Restaurants",
          subtitle: "Découvrez des cuisines maison et des restaurants traditionnels offrant des expériences culinaires uniques",
          browseRestaurants: "Parcourir Restaurants",
          becomePartner: "Devenir Partenaire",
          chooseRestaurantType: "Choisissez votre type de restaurant et commencez à gagner avec Lambalia",
          homeRestaurants: "Restaurants à Domicile",
          traditionalRestaurants: "Restaurants Traditionnels",
          intimateDining: "Repas intimes dans les foyers locaux",
          specialOrders: "Commandes spéciales et repas personnalisés",
          available: "disponible",
          specialOrdersCount: "commandes spéciales",
          noHomeRestaurants: "Aucun restaurant à domicile disponible pour le moment.",
          specialOrdersTitle: "Commandes Spéciales des Restaurants Traditionnels"
        },
        homeApplication: {
          title: "Candidature Restaurant à Domicile",
          personalInfo: "Informations Personnelles",
          legalName: "Nom Légal",
          phoneNumber: "Numéro de Téléphone",
          homeAddress: "Adresse du Domicile",
          city: "Ville",
          state: "État",
          postalCode: "Code Postal",
          country: "Pays",
          kitchenDescription: "Description de la Cuisine",
          kitchenDescriptionPlaceholder: "Décrivez votre cuisine, équipements et espace de cuisson",
          diningCapacity: "Capacité de Restauration",
          cuisineSpecialties: "Spécialités Culinaires",
          cuisineSpecialtiesPlaceholder: "ex., Italienne, Mexicaine, Végétalienne",
          dietaryAccommodations: "Aménagements Diététiques",
          dietaryAccommodationsPlaceholder: "ex., Sans gluten, Casher, Halal",
          foodHandlingExperience: "Avez-vous de l'expérience en manipulation d'aliments?",
          yearsCookingExperience: "Années d'Expérience Culinaire",
          liabilityInsurance: "Avez-vous une assurance responsabilité?",
          emergencyContactName: "Nom du Contact d'Urgence",
          emergencyContactPhone: "Téléphone du Contact d'Urgence",
          submitButton: "Soumettre Candidature",
          submitting: "Soumission Candidature...",
          successMessage: "Candidature soumise avec succès! Nous l'examinerons dans 3-5 jours ouvrables.",
          errorMessage: "Échec de soumission de candidature. Veuillez réessayer."
        },
        traditionalApplication: {
          title: "Candidature Restaurant Traditionnel",
          restaurantName: "Nom du Restaurant",
          businessLicenseNumber: "Numéro de Licence d'Entreprise",
          yearsInBusiness: "Années d'Activité",
          successMessage: "Candidature de restaurant soumise avec succès! Nous l'examinerons dans 5-7 jours ouvrables."
        }
      },

      eats: {
        title: "🍽️ Lambalia Eats",
        subtitle: "Marché de Nourriture en Temps Réel",
        tabs: {
          browse: "🛒 Parcourir Nourriture",
          request: "🍽️ Demander Nourriture",
          offer: "👩‍🍳 Offrir Nourriture", 
          orders: "📋 Mes Commandes",
          requests: "📤 Demandes Actives"
        },
        browse: {
          title: "🍳 Nourriture Disponible Près de Vous",
          refresh: "Actualiser",
          noOffers: "Aucune offre de nourriture à proximité",
          noOffersMessage: "Soyez le premier à publier un repas délicieux!",
          findingFood: "Trouver de la nourriture délicieuse près de vous..."
        }
      },

      charity: {
        title: "🤝❤️ Donner en Retour - Programme d'Impact Communautaire",
        subtitle: "Transformez votre cuisine en soutien communautaire et gagnez des avantages premium",
        overview: {
          title: "Impact Communautaire par la Nourriture",
          description: "Rejoignez notre programme communautaire où vos compétences culinaires aident à nourrir ceux dans le besoin tout en gagnant des avantages premium sur la plateforme.",
          impactStats: "Statistiques d'Impact Communautaire",
          totalMeals: "Total des Repas Fournis",
          activeVolunteers: "Volontaires Actifs",
          partneredOrganizations: "Organisations Partenaires",
          volunteersHours: "Heures de Bénévolat Ce Mois"
        },
        tiers: {
          communityHelper: {
            title: "Aide Communautaire",
            price: "Gratuit",
            commission: "Taux de Commission 15%",
            requirements: "Exigences:",
            req1: "4 heures mensuelles de bénévolat",
            req2: "2 activités caritatives", 
            req3: "10 livres de nourriture donnée mensuellement"
          },
          gardenSupporter: {
            title: "Soutien du Jardin", 
            price: "Gagné par le Service",
            commission: "Taux de Commission 12%",
            requirements: "Exigences:",
            req1: "8 heures mensuelles de bénévolat",
            req2: "4 activités caritatives",
            req3: "20 livres de nourriture donnée mensuellement"
          },
          communityChampion: {
            title: "Champion Communautaire",
            price: "Statut Elite",
            commission: "Taux de Commission 10%",
            requirements: "Exigences:",
            req1: "12 heures mensuelles de bénévolat",
            req2: "5 activités caritatives",
            req3: "30 livres de nourriture donnée mensuellement"
          }
        },
        benefits: {
          premiumBadge: "Badge Premium Communautaire",
          reducedCommission: "Taux de Commission Réduits",
          prioritySupport: "Support Client Prioritaire",
          featuredProfile: "Placement de Profil en Vedette",
          exclusiveEvents: "Événements Communautaires Exclusifs",
          advancedTools: "Outils Marketing Avancés",
          directMessaging: "Messagerie Directe Client",
          premiumPlacement: "Placement Premium de Produit",
          localChampion: "Badge de Champion Local"
        },
        registration: {
          title: "Rejoindre le Programme Communautaire",
          hoursPerMonth: "Heures Engagées Par Mois",
          charityTypes: "Types de Charité Préférés",
          locations: "Emplacements Préférés",
          impactGoal: "Objectif d'Impact Mensuel",
          submitButton: "Rejoindre le Programme 🌱",
          submitting: "Rejoindre le Programme..."
        },
        actions: {
          joinProgram: "Rejoindre le Programme Communautaire 🌱",
          submitActivity: "Soumettre Activité",
          viewDashboard: "Voir Tableau de Bord", 
          findOrganizations: "Trouver Organisations",
          calculateImpact: "Calculer Impact"
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
        fusion: "Fusion",
        comfortFood: "Nourriture Réconfortante",
        healthy: "Saine",
        vegan: "Végétalienne",
        desserts: "Desserts"
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

      auth: {
        login: "Anmelden",
        register: "Registrieren",
        logout: "Abmelden",
        email: "E-Mail",
        password: "Passwort",
        username: "Benutzername",
        fullName: "Vollständiger Name",
        postalCode: "Postleitzahl",
        loginButton: "Betreten Sie Ihre Küche 👨‍🍳",
        registerButton: "Der Gemeinschaft Beitreten",
        joinLambalia: "Lambalia Beitreten"
      },

      home: {
        title: "Lambalia",
        subtitle: "Schmecken Sie das Erbe der Welt",
        description: "Verbinden Sie sich mit leidenschaftlichen Heimköchen, entdecken Sie authentische Rezepte und verwandeln Sie Ihre Küche in ein globales kulinarisches Erlebnis."
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
        loginButton: "Entre na Sua Cozinha 👨‍🍳",
        registerButton: "Juntar-se à Comunidade",
        joinLambalia: "Junte-se ao Lambalia"
      },

      // Forms
      forms: {
        createSnippet: {
          title: "Criar Trecho de Receita",
          recipeTitle: "Título da Receita",
          recipeTitlePlaceholder: "Digite o nome da receita",
          localTitle: "Título Local",
          localTitlePlaceholder: "Nome da receita em seu idioma local (opcional)",
          description: "Descrição",
          descriptionPlaceholder: "Descreva sua receita",
          snippetType: "Tipo de Trecho",
          ingredients: "Ingredientes",
          ingredientName: "Ingrediente",
          amount: "Quantidade",
          unit: "Unidade",
          addIngredient: "Adicionar Ingrediente",
          preparationSteps: "Passos de Preparação",
          addStep: "Adicionar Passo",
          cookingTime: "Tempo de Cozimento (minutos)",
          difficultyLevel: "Nível de Dificuldade",
          servings: "Porções",
          tags: "Tags",
          tagsPlaceholder: "Adicionar tags (pressione Enter)",
          imageUpload: "Carregar Imagem",
          videoUpload: "Carregar Vídeo",
          submitButton: "Criar Trecho de Receita",
          submitting: "Criando...",
          dragDropImage: "Arraste e solte uma imagem aqui ou clique para selecionar",
          videoPlaceholder: "Carregue um vídeo curto do seu prato finalizado"
        },
        grocery: {
          title: "Encontrar Ingredientes Locais",
          subtitle: "Procure ingredientes em mercearias próximas e obtenha informações de preços",
          searchTitle: "Buscar Ingredientes",
          postalCode: "Seu CEP",
          postalCodePlaceholder: "Digite seu CEP",
          ingredientsLabel: "Ingredientes",
          ingredientPlaceholder: "ex: tomates, queijo, manjericão",
          addIngredient: "Adicionar Ingrediente",
          searchButton: "🔍 Buscar Lojas",
          searching: "Buscando...",
          distance: "Distância Máxima",
          budget: "Preferência de Orçamento",
          delivery: "Preferência de Entrega"
        }
      },

      restaurant: {
        marketplace: {
          title: "Mercado de Restaurantes",
          subtitle: "Descubra cozinhas caseiras e restaurantes tradicionais que oferecem experiências culinárias únicas",
          browseRestaurants: "Navegar Restaurantes",
          becomePartner: "Tornar-se Parceiro",
          homeRestaurants: "Restaurantes Caseiros",
          traditionalRestaurants: "Restaurantes Tradicionais",
          intimateDining: "Jantares íntimos em casas locais",
          specialOrders: "Pedidos especiais e refeições personalizadas",
          available: "disponível",
          specialOrdersCount: "pedidos especiais",
          noHomeRestaurants: "Nenhum restaurante caseiro disponível ainda.",
          specialOrdersTitle: "Pedidos Especiais de Restaurantes Tradicionais"
        },
        homeApplication: {
          title: "Candidatura Restaurante Domiciliar",
          personalInfo: "Informações Pessoais",
          legalName: "Nome Legal",
          phoneNumber: "Número de Telefone",
          homeAddress: "Endereço Residencial",
          city: "Cidade",
          state: "Estado",
          postalCode: "CEP",
          country: "País",
          kitchenDescription: "Descrição da Cozinha",
          kitchenDescriptionPlaceholder: "Descreva sua cozinha, equipamentos e espaço de cozimento",
          diningCapacity: "Capacidade de Jantar",
          cuisineSpecialties: "Especialidades Culinárias",
          cuisineSpecialtiesPlaceholder: "ex., Italiana, Mexicana, Vegana",
          dietaryAccommodations: "Acomodações Dietéticas",
          dietaryAccommodationsPlaceholder: "ex., Sem glúten, Kosher, Halal",
          foodHandlingExperience: "Você tem experiência em manuseio de alimentos?",
          yearsCookingExperience: "Anos de Experiência Culinária",
          liabilityInsurance: "Você tem seguro de responsabilidade civil?",
          emergencyContactName: "Nome do Contato de Emergência",
          emergencyContactPhone: "Telefone do Contato de Emergência",
          submitButton: "Enviar Candidatura",
          submitting: "Enviando Candidatura...",
          successMessage: "Candidatura enviada com sucesso! Analisaremos em 3-5 dias úteis.",
          errorMessage: "Falha ao enviar candidatura. Tente novamente."
        },
        traditionalApplication: {
          title: "Candidatura Restaurante Tradicional",
          restaurantName: "Nome do Restaurante",
          businessLicenseNumber: "Número da Licença Comercial",
          yearsInBusiness: "Anos em Atividade",
          successMessage: "Candidatura de restaurante enviada com sucesso! Analisaremos em 5-7 dias úteis."
        }
      },

      cuisines: {
        american: "Americana",
        mexican: "Mexicana",
        italian: "Italiana",
        chinese: "Chinesa",
        indian: "Indiana",
        japanese: "Japonesa",
        thai: "Tailandesa", 
        mediterranean: "Mediterrânea",
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
        loginButton: "Войдите в Вашу Кухню 👨‍🍳",
        registerButton: "Присоединиться к Сообществу",
        joinLambalia: "Присоединиться к Lambalia"
      },

      // Forms
      forms: {
        createSnippet: {
          title: "Создать Фрагмент Рецепта",
          recipeTitle: "Название Рецепта",
          recipeTitlePlaceholder: "Введите название рецепта",
          localTitle: "Местное Название",
          localTitlePlaceholder: "Название рецепта на вашем местном языке (необязательно)",
          description: "Описание",
          descriptionPlaceholder: "Опишите ваш рецепт",
          snippetType: "Тип Фрагмента",
          ingredients: "Ингредиенты",
          ingredientName: "Ингредиент",
          amount: "Количество",
          unit: "Единица",
          addIngredient: "Добавить Ингредиент",
          preparationSteps: "Шаги Приготовления",
          addStep: "Добавить Шаг",
          cookingTime: "Время Готовки (минуты)",
          difficultyLevel: "Уровень Сложности",
          servings: "Порции",
          tags: "Теги",
          tagsPlaceholder: "Добавить теги (нажмите Enter)",
          imageUpload: "Загрузить Изображение",
          videoUpload: "Загрузить Видео",
          submitButton: "Создать Фрагмент Рецепта",
          submitting: "Создание...",
          dragDropImage: "Перетащите изображение сюда или нажмите для выбора",
          videoPlaceholder: "Загрузите короткое видео вашего готового блюда"
        },
        grocery: {
          title: "Найти Местные Ингредиенты",
          subtitle: "Ищите ингредиенты в близлежащих продуктовых магазинах и получайте ценовую информацию",
          searchTitle: "Поиск Ингредиентов",
          postalCode: "Ваш Почтовый Индекс",
          postalCodePlaceholder: "Введите ваш почтовый индекс",
          ingredientsLabel: "Ингредиенты",
          ingredientPlaceholder: "напр., помидоры, сыр, базилик",
          addIngredient: "Добавить Ингредиент",
          searchButton: "🔍 Поиск Магазинов",
          searching: "Поиск...",
          distance: "Максимальное Расстояние",
          budget: "Предпочтение Бюджета",
          delivery: "Предпочтение Доставки"
        }
      },

      restaurant: {
        marketplace: {
          title: "Рынок Ресторанов",
          subtitle: "Откройте для себя домашние кухни и традиционные рестораны, предлагающие уникальные кулинарные впечатления",
          browseRestaurants: "Просмотр Ресторанов",
          becomePartner: "Стать Партнером",
          homeRestaurants: "Домашние Рестораны",
          traditionalRestaurants: "Традиционные Рестораны",
          intimateDining: "Интимные обеды в местных домах",
          specialOrders: "Специальные заказы и индивидуальные блюда",
          available: "доступно",
          specialOrdersCount: "специальные заказы",
          noHomeRestaurants: "Домашних ресторанов пока нет.",
          specialOrdersTitle: "Специальные Заказы от Традиционных Ресторанов"
        },
        homeApplication: {
          title: "Заявка на Домашний Ресторан",
          personalInfo: "Личная Информация",
          legalName: "Юридическое Имя",
          phoneNumber: "Номер Телефона",
          homeAddress: "Домашний Адрес",
          city: "Город",
          state: "Область",
          postalCode: "Почтовый Индекс",
          country: "Страна",
          kitchenDescription: "Описание Кухни",
          kitchenDescriptionPlaceholder: "Опишите вашу кухню, оборудование и зону приготовления",
          diningCapacity: "Вместимость Обеденной Зоны",
          cuisineSpecialties: "Кулинарные Специальности",
          cuisineSpecialtiesPlaceholder: "напр., Итальянская, Мексиканская, Веганская",
          dietaryAccommodations: "Диетические Приспособления",
          dietaryAccommodationsPlaceholder: "напр., Безглютеновая, Кошерная, Халяль",
          foodHandlingExperience: "Есть ли у вас опыт обращения с продуктами?",
          yearsCookingExperience: "Лет Кулинарного Опыта",
          liabilityInsurance: "Есть ли у вас страхование ответственности?",
          emergencyContactName: "Имя Контакта Экстренной Связи",
          emergencyContactPhone: "Телефон Контакта Экстренной Связи",
          submitButton: "Подать Заявку",
          submitting: "Подача Заявки...",
          successMessage: "Заявка успешно подана! Мы рассмотрим её в течение 3-5 рабочих дней.",
          errorMessage: "Не удалось подать заявку. Пожалуйста, попробуйте снова."
        },
        traditionalApplication: {
          title: "Заявка Традиционного Ресторана",
          restaurantName: "Название Ресторана",
          businessLicenseNumber: "Номер Бизнес-лицензии",
          yearsInBusiness: "Лет в Бизнесе",
          successMessage: "Заявка ресторана успешно подана! Мы рассмотрим её в течение 5-7 рабочих дней."
        }
      },

      cuisines: {
        american: "Американская",
        mexican: "Мексиканская",
        italian: "Итальянская",
        chinese: "Китайская",
        indian: "Индийская",
        japanese: "Японская",
        thai: "Тайская",
        mediterranean: "Средиземноморская",
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
        loginButton: "Entra nella Tua Cucina 👨‍🍳",
        registerButton: "Unisciti alla Comunità",
        joinLambalia: "Unisciti a Lambalia"
      },

      // Forms
      forms: {
        createSnippet: {
          title: "Crea Frammento di Ricetta",
          recipeTitle: "Titolo della Ricetta",
          recipeTitlePlaceholder: "Inserisci il nome della ricetta",
          localTitle: "Titolo Locale",
          localTitlePlaceholder: "Nome della ricetta nella tua lingua locale (opzionale)",
          description: "Descrizione",
          descriptionPlaceholder: "Descrivi la tua ricetta",
          snippetType: "Tipo di Frammento",
          ingredients: "Ingredienti",
          ingredientName: "Ingrediente",
          amount: "Quantità",
          unit: "Unità",
          addIngredient: "Aggiungi Ingrediente",
          preparationSteps: "Passi di Preparazione",
          addStep: "Aggiungi Passo",
          cookingTime: "Tempo di Cottura (minuti)",
          difficultyLevel: "Livello di Difficoltà",
          servings: "Porzioni",
          tags: "Tag",
          tagsPlaceholder: "Aggiungi tag (premi Invio)",
          imageUpload: "Carica Immagine",
          videoUpload: "Carica Video",
          submitButton: "Crea Frammento di Ricetta",
          submitting: "Creazione...",
          dragDropImage: "Trascina e rilascia un'immagine qui o clicca per selezionare",
          videoPlaceholder: "Carica un breve video del tuo piatto finito"
        },
        grocery: {
          title: "Trova Ingredienti Locali",
          subtitle: "Cerca ingredienti nei negozi di alimentari nelle vicinanze e ottieni informazioni sui prezzi",
          searchTitle: "Cerca Ingredienti",
          postalCode: "Il Tuo Codice Postale",
          postalCodePlaceholder: "Inserisci il tuo codice postale",
          ingredientsLabel: "Ingredienti",
          ingredientPlaceholder: "es: pomodori, formaggio, basilico",
          addIngredient: "Aggiungi Ingrediente",
          searchButton: "🔍 Cerca Negozi",
          searching: "Ricerca...",
          distance: "Distanza Massima",
          budget: "Preferenza di Budget",
          delivery: "Preferenza di Consegna"
        }
      },

      restaurant: {
        marketplace: {
          title: "Mercato Ristoranti",
          subtitle: "Scopri cucine casalinghe e ristoranti tradizionali che offrono esperienze culinarie uniche",
          browseRestaurants: "Sfoglia Ristoranti",
          becomePartner: "Diventa Partner",
          homeRestaurants: "Ristoranti Casalinghi",
          traditionalRestaurants: "Ristoranti Tradizionali",
          intimateDining: "Cene intime in case locali",
          specialOrders: "Ordini speciali e pasti personalizzati",
          available: "disponibile",
          specialOrdersCount: "ordini speciali",
          noHomeRestaurants: "Nessun ristorante casalingo disponibile ancora.",
          specialOrdersTitle: "Ordini Speciali da Ristoranti Tradizionali"
        },
        homeApplication: {
          title: "Candidatura Ristorante Domestico",
          personalInfo: "Informazioni Personali",
          legalName: "Nome Legale",
          phoneNumber: "Numero di Telefono",
          homeAddress: "Indirizzo di Casa",
          city: "Città",
          state: "Stato",
          postalCode: "Codice Postale",
          country: "Paese",
          kitchenDescription: "Descrizione della Cucina",
          kitchenDescriptionPlaceholder: "Descrivi la tua cucina, attrezzature e spazio di cottura",
          diningCapacity: "Capacità Sala da Pranzo",
          cuisineSpecialties: "Specialità Culinarie",
          cuisineSpecialtiesPlaceholder: "es., Italiana, Messicana, Vegana",
          dietaryAccommodations: "Adattamenti Dietetici",
          dietaryAccommodationsPlaceholder: "es., Senza glutine, Kosher, Halal",
          foodHandlingExperience: "Hai esperienza nella manipolazione degli alimenti?",
          yearsCookingExperience: "Anni di Esperienza Culinaria",
          liabilityInsurance: "Hai un'assicurazione di responsabilità civile?",
          emergencyContactName: "Nome Contatto di Emergenza",
          emergencyContactPhone: "Telefono Contatto di Emergenza",
          submitButton: "Invia Candidatura",
          submitting: "Invio Candidatura...",
          successMessage: "Candidatura inviata con successo! La esamineremo entro 3-5 giorni lavorativi.",
          errorMessage: "Invio candidatura fallito. Riprova."
        },
        traditionalApplication: {
          title: "Candidatura Ristorante Tradizionale",
          restaurantName: "Nome Ristorante",
          businessLicenseNumber: "Numero Licenza Commerciale",
          yearsInBusiness: "Anni di Attività",
          successMessage: "Candidatura ristorante inviata con successo! La esamineremo entro 5-7 giorni lavorativi."
        }
      },

      cuisines: {
        american: "Americana",
        mexican: "Messicana",
        italian: "Italiana",
        chinese: "Cinese",
        indian: "Indiana",
        japanese: "Giapponese",
        thai: "Tailandese",
        mediterranean: "Mediterranea"
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
      
      common: {
        loading: "جاري التحميل...",
        submit: "إرسال",
        cancel: "إلغاء",
        save: "حفظ",
        edit: "تعديل",
        delete: "حذف",
        search: "بحث",
        filter: "فلترة",
        sort: "ترتيب",
        back: "عودة",
        next: "التالي",
        previous: "السابق",
        close: "إغلاق",
        open: "فتح",
        yes: "نعم",
        no: "لا",
        ok: "موافق",
        error: "خطأ",
        success: "نجح",
        warning: "تحذير",
        info: "معلومات"
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
        forgotPassword: "نسيت كلمة المرور؟",
        rememberMe: "تذكرني",
        loginButton: "ادخل إلى مطبخك 👨‍🍳",
        registerButton: "انضم للمجتمع",
        joinLambalia: "انضم إلى لامباليا",
        welcomeMessage: "انضم لمجتمعنا من الطهاة المنزليين الذين يشاركون الوصفات الأصيلة من جميع أنحاء العالم!"
      },

      home: {
        title: "لامباليا",
        subtitle: "تذوق تراث العالم",
        welcomeMessage: "انضم لمجتمعنا من الطهاة المنزليين الذين يشاركون الوصفات الأصيلة من جميع أنحاء العالم!",
        description: "تواصل مع الطهاة المنزليين المتحمسين، اكتشف الوصفات الأصيلة، وحول مطبخك إلى تجربة طهي عالمية.",
        features: {
          recipes: "198+ وصفة تقليدية",
          monetize: "استثمر مهاراتك في الطبخ",
          restaurant: "منصة المطعم المنزلي",
          communities: "80+ مجتمع ثقافي",
          heritageRecipes: "وصفات التراث",
          specialtyIngredients: "المكونات المتخصصة"
        },
        actions: {
          browseName: "📚 تصفح القوالب",
          createName: "✨ إنشاء مقطع",
          ingredientsName: "🛒 البحث عن المكونات", 
          restaurantName: "🏠👩‍🍳 فتح المطبخ",
          marketplaceName: "🌱🛒 السوق المحلي",
          charityName: "🤝❤️ العطاء",
          eatsName: "🚚🍽️ الطعام السريع"
        },
        cookingClasses: {
          title: "دروس الطبخ عبر الإنترنت",
          description: "تعلم من الطهاة الخبراء حول العالم",
          learnMore: "اعرف المزيد"
        },
        recipeSnippets: {
          title: "أحدث مقاطع الوصفات",
          subtitle: "نصائح طبخ سريعة من مجتمعنا",
          viewAll: "عرض جميع المقاطع",
          cookingTip: "نصيحة الطبخ",
          noSnippets: "لم يتم العثور على مقاطع وصفات. كن أول من يشارك مقطع وصفتك التقليدية على لامباليا!"
        },
        communityStats: {
          title: "انضم لمجتمعنا العالمي للطبخ",
          activeChefs: "الطهاة المنزليون النشطون",
          countriesServed: "البلدان المخدومة",
          recipesShared: "الوصفات المشاركة",
          culturesRepresented: "الثقافات الممثلة"
        }
      },

      // Forms
      forms: {
        createSnippet: {
          title: "إنشاء مقطع الوصفة",
          recipeTitle: "عنوان الوصفة",
          recipeTitlePlaceholder: "أدخل اسم الوصفة",
          localTitle: "العنوان المحلي",
          localTitlePlaceholder: "اسم الوصفة بلغتك المحلية (اختياري)",
          description: "الوصف",
          descriptionPlaceholder: "اوصف وصفتك",
          snippetType: "نوع المقطع",
          ingredients: "المكونات",
          ingredientName: "المكون",
          amount: "الكمية",
          unit: "الوحدة",
          addIngredient: "إضافة مكون",
          preparationSteps: "خطوات التحضير",
          addStep: "إضافة خطوة",
          cookingTime: "وقت الطبخ (دقائق)",
          difficultyLevel: "مستوى الصعوبة",
          servings: "عدد الحصص",
          tags: "العلامات",
          tagsPlaceholder: "إضافة علامات (اضغط Enter)",
          imageUpload: "رفع صورة",
          videoUpload: "رفع فيديو",
          submitButton: "إنشاء مقطع الوصفة",
          submitting: "جاري الإنشاء...",
          dragDropImage: "اسحب وأفلت صورة هنا أو انقر للاختيار",
          videoPlaceholder: "ارفع فيديو قصير لطبقك المكتمل"
        },
        grocery: {
          title: "البحث عن المكونات المحلية",
          subtitle: "ابحث عن المكونات في محلات البقالة القريبة واحصل على معلومات الأسعار",
          searchTitle: "البحث عن المكونات",
          postalCode: "رمزك البريدي",
          postalCodePlaceholder: "أدخل رمزك البريدي",
          ingredientsLabel: "المكونات",
          ingredientPlaceholder: "مثل: طماطم، جبن، ريحان",
          addIngredient: "إضافة مكون",
          searchButton: "🔍 البحث عن المتاجر",
          searching: "جاري البحث...",
          distance: "أقصى مسافة",
          budget: "تفضيل الميزانية",
          delivery: "تفضيل التوصيل"
        }
      },

      restaurant: {
        marketplace: {
          title: "سوق المطاعم",
          subtitle: "اكتشف المطابخ المنزلية والمطاعم التقليدية التي تقدم تجارب طبخ فريدة",
          browseRestaurants: "تصفح المطاعم",
          becomePartner: "كن شريكاً",
          homeRestaurants: "المطاعم المنزلية",
          traditionalRestaurants: "المطاعم التقليدية",
          intimateDining: "وجبات حميمة في المنازل المحلية",
          specialOrders: "طلبات خاصة ووجبات مخصصة",
          available: "متاح",
          specialOrdersCount: "طلبات خاصة",
          noHomeRestaurants: "لا توجد مطاعم منزلية متاحة بعد.",
          specialOrdersTitle: "الطلبات الخاصة من المطاعم التقليدية"
        },
        homeApplication: {
          title: "طلب مطعم منزلي",
          personalInfo: "المعلومات الشخصية",
          legalName: "الاسم القانوني",
          phoneNumber: "رقم الهاتف",
          homeAddress: "عنوان المنزل",
          city: "المدينة",
          state: "الولاية",
          postalCode: "الرمز البريدي",
          country: "البلد",
          kitchenDescription: "وصف المطبخ",
          kitchenDescriptionPlaceholder: "اوصف مطبخك والمعدات ومساحة الطبخ",
          diningCapacity: "سعة منطقة الطعام",
          cuisineSpecialties: "التخصصات الطبخية",
          cuisineSpecialtiesPlaceholder: "مثل، إيطالية، مكسيكية، نباتية",
          dietaryAccommodations: "التكيفات الغذائية",
          dietaryAccommodationsPlaceholder: "مثل، خالي من الغلوتين، كوشير، حلال",
          foodHandlingExperience: "هل لديك خبرة في التعامل مع الطعام؟",
          yearsCookingExperience: "سنوات الخبرة في الطبخ",
          liabilityInsurance: "هل لديك تأمين مسؤولية؟",
          emergencyContactName: "اسم جهة الاتصال الطارئ",
          emergencyContactPhone: "هاتف جهة الاتصال الطارئ",
          submitButton: "إرسال الطلب",
          submitting: "جاري إرسال الطلب...",
          successMessage: "تم إرسال الطلب بنجاح! سنراجعه خلال 3-5 أيام عمل.",
          errorMessage: "فشل في إرسال الطلب. يرجى المحاولة مرة أخرى."
        },
        traditionalApplication: {
          title: "طلب مطعم تقليدي",
          restaurantName: "اسم المطعم",
          businessLicenseNumber: "رقم رخصة العمل",
          yearsInBusiness: "سنوات العمل",
          successMessage: "تم إرسال طلب المطعم بنجاح! سنراجعه خلال 5-7 أيام عمل."
        }
      },

      cuisines: {
        american: "أمريكية",
        mexican: "مكسيكية",
        italian: "إيطالية",
        chinese: "صينية",
        indian: "هندية",
        japanese: "يابانية",
        thai: "تايلاندية",
        mediterranean: "متوسطية",
        african: "أفريقية",
        middleEastern: "شرق أوسطية",
        caribbean: "كاريبية"
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
      
      common: {
        loading: "लोड हो रहा है...",
        submit: "जमा करें",
        cancel: "रद्द करें",
        save: "सहेजें",
        edit: "संपादित करें",
        delete: "हटाएं",
        search: "खोजें",
        filter: "फ़िल्टर",
        sort: "क्रमबद्ध करें",
        back: "वापस",
        next: "अगला",
        previous: "पिछला",
        close: "बंद करें",
        open: "खोलें",
        yes: "हां",
        no: "नहीं",
        ok: "ठीक है",
        error: "त्रुटि",
        success: "सफल",
        warning: "चेतावनी",
        info: "जानकारी"
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
        forgotPassword: "पासवर्ड भूल गए?",
        rememberMe: "मुझे याद रखें",
        loginButton: "अपनी रसोई में प्रवेश करें 👨‍🍳",
        registerButton: "समुदाय में शामिल हों",
        joinLambalia: "लैम्बालिया में शामिल हों",
        welcomeMessage: "दुनिया भर के प्रामाणिक व्यंजनों को साझा करने वाले घरेलू रसोइयों के हमारे समुदाय में शामिल हों!"
      },

      home: {
        title: "लैम्बालिया",
        subtitle: "अपनी रसोई को एक वैश्विक पाक अनुभव में बदलें",
        welcomeMessage: "लैम्बालिया में आपका स्वागत है - जहां हर सांस्कृतिक व्यंजन अपनी आवाज़ पाता है",
        description: "भावुक घरेलू रसोइयों से जुड़ें, प्रामाणिक व्यंजनों की खोज करें, और अपनी रसोई को एक वैश्विक पाक अनुभव में बदलें।",
        features: {
          recipes: "198+ पारंपरिक व्यंजन",
          monetize: "अपनी खाना पकाने की कला से कमाई करें",
          restaurant: "होम रेस्टोरेंट प्लेटफ़ॉर्म",
          communities: "80+ सांस्कृतिक समुदाय",
          heritageRecipes: "विरासती व्यंजन",
          specialtyIngredients: "विशेष सामग्री"
        },
        actions: {
          browseName: "📚 टेम्प्लेट ब्राउज़ करें",
          createName: "✨ स्निपेट बनाएं",
          ingredientsName: "🛒 सामग्री खोजें", 
          restaurantName: "🏠👩‍🍳 रसोई खोलें",
          marketplaceName: "🌱🛒 स्थानीय बाजार",
          charityName: "🤝❤️ वापस दें",
          eatsName: "🚚🍽️ तुरंत खाना"
        },
        cookingClasses: {
          title: "ऑनलाइन खाना पकाने की कक्षाएं",
          description: "दुनिया भर के मास्टर शेफ़ से सीखें",
          learnMore: "और जानें"
        },
        recipeSnippets: {
          title: "नवीनतम रेसिपी स्निपेट्स",
          subtitle: "हमारे समुदाय से त्वरित खाना पकाने की युक्तियां",
          viewAll: "सभी स्निपेट्स देखें",
          cookingTip: "खाना पकाने की टिप",
          noSnippets: "कोई रेसिपी स्निपेट्स नहीं मिले। लैम्बालिया पर अपना पारंपरिक रेसिपी स्निपेट साझा करने वाले पहले व्यक्ति बनें!"
        },
        communityStats: {
          title: "हमारे वैश्विक पाक समुदाय में शामिल हों",
          activeChefs: "सक्रिय घरेलू रसोइए",
          countriesServed: "सेवा प्रदान किए गए देश",
          recipesShared: "साझा किए गए व्यंजन",
          culturesRepresented: "प्रतिनिधित्व की गई संस्कृतियां"
        }
      },

      // Forms
      forms: {
        createSnippet: {
          title: "रेसिपी स्निपेट बनाएं",
          recipeTitle: "रेसिपी का शीर्षक",
          recipeTitlePlaceholder: "रेसिपी का नाम दर्ज करें",
          localTitle: "स्थानीय शीर्षक",
          localTitlePlaceholder: "अपनी स्थानीय भाषा में रेसिपी का नाम (वैकल्पिक)",
          description: "विवरण",
          descriptionPlaceholder: "अपनी रेसिपी का वर्णन करें",
          snippetType: "स्निपेट का प्रकार",
          ingredients: "सामग्री",
          ingredientName: "सामग्री",
          amount: "मात्रा",
          unit: "इकाई",
          addIngredient: "सामग्री जोड़ें",
          preparationSteps: "तैयारी के चरण",
          addStep: "चरण जोड़ें",
          cookingTime: "पकाने का समय (मिनट)",
          difficultyLevel: "कठिनाई का स्तर",
          servings: "सर्विंग्स",
          tags: "टैग",
          tagsPlaceholder: "टैग जोड़ें (Enter दबाएं)",
          imageUpload: "छवि अपलोड करें",
          videoUpload: "वीडियो अपलोड करें",
          submitButton: "रेसिपी स्निपेट बनाएं",
          submitting: "बना रहे हैं...",
          dragDropImage: "यहां छवि खींचें और छोड़ें या चुनने के लिए क्लिक करें",
          videoPlaceholder: "अपने तैयार व्यंजन का छोटा वीडियो अपलोड करें"
        },
        grocery: {
          title: "स्थानीय सामग्री खोजें",
          subtitle: "नजदीकी किराना दुकानों में सामग्री खोजें और मूल्य जानकारी प्राप्त करें",
          searchTitle: "सामग्री खोजें",
          postalCode: "आपका पिन कोड",
          postalCodePlaceholder: "अपना पिन कोड दर्ज करें",
          ingredientsLabel: "सामग्री",
          ingredientPlaceholder: "जैसे: टमाटर, पनीर, तुलसी",
          addIngredient: "सामग्री जोड़ें",
          searchButton: "🔍 दुकानें खोजें",
          searching: "खोज रहे हैं...",
          distance: "अधिकतम दूरी",
          budget: "बजट प्राथमिकता",
          delivery: "डिलीवरी प्राथमिकता"
        }
      },

      restaurant: {
        marketplace: {
          title: "रेस्टोरेंट बाजार",
          subtitle: "घरेलू रसोई और पारंपरिक रेस्टोरेंट खोजें जो अनोखे पाक अनुभव प्रदान करते हैं",
          browseRestaurants: "रेस्टोरेंट ब्राउज़ करें",
          becomePartner: "साझीदार बनें",
          homeRestaurants: "होम रेस्टोरेंट",
          traditionalRestaurants: "पारंपरिक रेस्टोरेंट",
          intimateDining: "स्थानीय घरों में अंतरंग भोजन",
          specialOrders: "विशेष ऑर्डर और कस्टम भोजन",
          available: "उपलब्ध",
          specialOrdersCount: "विशेष ऑर्डर",
          noHomeRestaurants: "अभी तक कोई होम रेस्टोरेंट उपलब्ध नहीं।",
          specialOrdersTitle: "पारंपरिक रेस्टोरेंट से विशेष ऑर्डर"
        },
        homeApplication: {
          title: "होम रेस्टोरेंट आवेदन",
          personalInfo: "व्यक्तिगत जानकारी",
          legalName: "कानूनी नाम",
          phoneNumber: "फोन नंबर",
          homeAddress: "घर का पता",
          city: "शहर",
          state: "राज्य",
          postalCode: "पिन कोड",
          country: "देश",
          kitchenDescription: "रसोई विवरण",
          kitchenDescriptionPlaceholder: "अपनी रसोई, उपकरण और खाना पकाने की जगह का वर्णन करें",
          diningCapacity: "भोजन क्षमता",
          cuisineSpecialties: "पाक विशेषताएं",
          cuisineSpecialtiesPlaceholder: "जैसे, इतालवी, मैक्सिकन, शाकाहारी",
          dietaryAccommodations: "आहार अनुकूलन",
          dietaryAccommodationsPlaceholder: "जैसे, ग्लूटेन-फ्री, कोशेर, हलाल",
          foodHandlingExperience: "क्या आपके पास भोजन संभालने का अनुभव है?",
          yearsCookingExperience: "खाना पकाने के अनुभव के वर्ष",
          liabilityInsurance: "क्या आपके पास देयता बीमा है?",
          emergencyContactName: "आपातकालीन संपर्क नाम",
          emergencyContactPhone: "आपातकालीन संपर्क फोन",
          submitButton: "आवेदन जमा करें",
          submitting: "आवेदन जमा कर रहे हैं...",
          successMessage: "आवेदन सफलतापूर्वक जमा किया गया! हम इसे 3-5 कार्य दिवसों में देखेंगे।",
          errorMessage: "आवेदन जमा करने में विफल। कृपया पुनः प्रयास करें।"
        },
        traditionalApplication: {
          title: "पारंपरिक रेस्टोरेंट आवेदन",
          restaurantName: "रेस्टोरेंट का नाम",
          businessLicenseNumber: "व्यावसायिक लाइसेंस नंबर",
          yearsInBusiness: "व्यवसाय के वर्ष",
          successMessage: "रेस्टोरेंट आवेदन सफलतापूर्वक जमा किया गया! हम इसे 5-7 कार्य दिवसों में देखेंगे।"
        }
      },

      cuisines: {
        american: "अमेरिकी",
        mexican: "मेक्सिकन",
        italian: "इतालवी",
        chinese: "चीनी",
        indian: "भारतीय",
        japanese: "जापानी",
        thai: "थाई",
        mediterranean: "भूमध्यसागरीय",
        african: "अफ्रीकी",
        middleEastern: "मध्य पूर्वी",
        caribbean: "कैरिबियन"
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