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

      // Lambalia Eats
      eats: {
        title: "🍽️ Lambalia Eats",
        subtitle: "Real-time Food Marketplace",
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
          title: "🍽️ Request Food",
          subtitle: "Tell local cooks what you're craving!",
          dishName: "What do you want to eat?",
          dishPlaceholder: "e.g., Chicken Biryani, Fresh Pasta",
          cuisineType: "Cuisine Type",
          description: "Description",
          descPlaceholder: "Describe how you'd like it prepared, any special preferences...",
          maxPrice: "Max Price ($)",
          maxWaitTime: "Max Wait Time (minutes)",
          servicePrefs: "Service Preferences",
          postButton: "Post Food Request 🍽️",
          posting: "Posting Request... ⏳"
        },
        offer: {  
          title: "👩‍🍳 Offer Food",
          subtitle: "Share your delicious homemade meal with hungry neighbors!",
          dishName: "Dish Name",
          dishPlaceholder: "e.g., Grandma's Chicken Curry",
          description: "Description", 
          descPlaceholder: "Describe your dish, cooking method, what makes it special...",
          quantity: "Quantity Available",
          pricePerServing: "Price per Serving ($)",
          deliveryFee: "Delivery Fee ($)",
          readyAt: "Ready At",
          availableUntil: "Available Until",
          serviceOptions: "Service Options",
          postButton: "Post Food Offer 👩‍🍳",
          posting: "Posting Offer... ⏳"
        },
        orders: {
          title: "📋 My Orders",
          noOrders: "No orders yet",
          noOrdersMessage: "Start by browsing available food or posting a request!",
          role: "Role",
          service: "Service", 
          total: "Total",
          tracking: "Tracking",
          ordered: "Ordered"
        },
        stats: {
          liveOrders: "live orders",
          cooksOnline: "cooks online",
          activeOffers: "Active Offers",
          activeRequests: "Active Requests", 
          ordersInProgress: "Orders in Progress",
          availableCooks: "Available Cooks"
        },
        serviceTypes: {
          pickup: "Pickup",
          delivery: "Delivery",
          dineIn: "Dine-in",
          pickupDesc: "You pick up, pay meal only",
          deliveryDesc: "Delivered to you, pay meal + delivery", 
          dineInDesc: "Eat at cook's place"
        },
        orderNow: "Order Now",
        details: "Details",
        acceptRequest: "Accept Request"
      },

      // Local Marketplace
      marketplace: {
        title: "Local Harvest Marketplace",
        subtitle: "Discover fresh, homegrown produce from your neighbors. From backyard tomatoes to small farm specialties.",
        tabs: {
          browse: "🛒 Browse Local",
          sell: "🌱 Sell Produce", 
          charity: "🤝 Give Back",
          impact: "🌍 Our Impact"
        },
        search: "🔍 Search Local Growers",
        allGrowers: "All Growers",
        backyardGardeners: "Backyard Gardeners",
        localFarms: "Local Farms",
        organicGrowers: "Organic Growers",
        hobbyFarmers: "Hobby Farmers"
      },

      // Charity Program
      charity: {
        title: "🤝 Community Food Sharing Program",
        subtitle: "Transform food waste into community support while earning premium membership benefits",
        tabs: {
          overview: "🌟 Overview",
          register: "📝 Register", 
          submit: "📋 Submit Activity",
          dashboard: "🎯 Dashboard",
          organizations: "🏪 Organizations"
        },
        howItWorks: "🌱 How It Works",
        premiumTiers: "🎖️ Premium Membership Tiers",
        joinProgram: "Join Community Program 🌱",
        startMakingDifference: "Start making a difference in your community today!"
      },

      // Cuisines
      // Forms
      forms: {
        createSnippet: {
          title: "Create Recipe Snippet",
          recipeTitle: "Recipe Title",
          recipeTitlePlaceholder: "Enter the recipe name",
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
          distance: "Max Distance",
          budget: "Budget Preference",
          delivery: "Delivery Preference"
        },
        restaurant: {
          homeApplication: {
            title: "Home Restaurant Application",
            personalInfo: "Personal Information",
            legalName: "Legal Name",
            phoneNumber: "Phone Number",
            homeAddress: "Home Address",
            city: "City",
            state: "State",
            postalCode: "Postal Code",
            country: "Country",
            kitchenDescription: "Kitchen Description",
            kitchenDescriptionPlaceholder: "Describe your kitchen setup, equipment, and cooking space",
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
            successMessage: "Application submitted successfully! We will review it within 3-5 business days.",
            errorMessage: "Failed to submit application. Please try again."
          },
          traditionalApplication: {
            title: "Traditional Restaurant Application",
            restaurantName: "Restaurant Name",
            businessLicenseNumber: "Business License Number",
            yearsInBusiness: "Years in Business",
            successMessage: "Restaurant application submitted successfully! We will review it within 5-7 business days."
          }
        }
      },

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
        }
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
        comfortFood: "Cuisine Réconfortante",
        healthy: "Sain",
        vegan: "Végétalien",
        desserts: "Desserts"
      }
    }
  },

  de: {
    translation: {
      nav: {
        browse: "Vorlagen Durchsuchen",
        create: "Ausschnitt Erstellen",
        ingredients: "Zutaten Finden",
        restaurant: "Küche Öffnen",
        marketplace: "Lokaler Markt", 
        charity: "Zurückgeben",
        eats: "Schnelles Essen",
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

      // Forms
      forms: {
        createSnippet: {
          title: "Rezept-Ausschnitt Erstellen",
          recipeTitle: "Rezept-Titel",
          recipeTitlePlaceholder: "Geben Sie den Rezeptnamen ein",
          localTitle: "Lokaler Titel",
          localTitlePlaceholder: "Rezeptname in Ihrer Lokalsprache (optional)",
          description: "Beschreibung",
          descriptionPlaceholder: "Beschreiben Sie Ihr Rezept",
          snippetType: "Ausschnitt-Typ",
          ingredients: "Zutaten",
          ingredientName: "Zutat",
          amount: "Menge",
          unit: "Einheit",
          addIngredient: "Zutat Hinzufügen",
          preparationSteps: "Zubereitungsschritte",
          addStep: "Schritt Hinzufügen",
          cookingTime: "Kochzeit (Minuten)",
          difficultyLevel: "Schwierigkeitsgrad",
          servings: "Portionen",
          tags: "Tags",
          tagsPlaceholder: "Tags hinzufügen (Enter drücken)",
          imageUpload: "Bild Hochladen",
          videoUpload: "Video Hochladen",
          submitButton: "Rezept-Ausschnitt Erstellen",
          submitting: "Erstellen...",
          dragDropImage: "Bild hier hineinziehen oder klicken zum Auswählen",
          videoPlaceholder: "Kurzes Video Ihres fertigen Gerichts hochladen"
        },
        grocery: {
          title: "Lokale Zutaten Finden",
          subtitle: "Suchen Sie nach Zutaten in nahegelegenen Lebensmittelgeschäften und erhalten Sie Preisinformationen",
          searchTitle: "Zutaten Suchen",
          postalCode: "Ihre Postleitzahl",
          postalCodePlaceholder: "Geben Sie Ihre Postleitzahl ein",
          ingredientsLabel: "Zutaten",
          ingredientPlaceholder: "z.B. Tomaten, Käse, Basilikum",
          addIngredient: "Zutat Hinzufügen",
          searchButton: "🔍 Geschäfte Suchen",
          searching: "Suchen...",
          distance: "Maximale Entfernung",
          budget: "Budget-Präferenz",
          delivery: "Lieferung-Präferenz"
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

  zh: {
    translation: {
      nav: {
        browse: "浏览模板",
        create: "创建片段", 
        ingredients: "寻找食材",
        restaurant: "开放厨房",
        marketplace: "本地市场",
        charity: "回馈社会",
        eats: "快餐",
        profile: "个人资料"
      },

      auth: {
        login: "登录",
        register: "注册",
        logout: "退出",
        email: "邮箱",
        password: "密码",
        username: "用户名",
        fullName: "全名",
        postalCode: "邮政编码",
        loginButton: "进入您的厨房 👨‍🍳",
        registerButton: "加入社区",
        joinLambalia: "加入 Lambalia"
      },

      cuisines: {
        american: "美式",
        mexican: "墨西哥菜",
        italian: "意大利菜", 
        chinese: "中华料理",
        indian: "印度菜",
        japanese: "日式料理",
        thai: "泰式料理",
        mediterranean: "地中海菜"
      }
    }
  },

  ja: {
    translation: {
      nav: {
        browse: "テンプレートを見る",
        create: "スニペット作成",
        ingredients: "食材を探す",
        restaurant: "キッチンを開く",
        marketplace: "ローカルマーケット",
        charity: "社会貢献",
        eats: "クイック料理",
        profile: "プロフィール"
      },

      auth: {
        login: "ログイン", 
        register: "登録",
        logout: "ログアウト",
        email: "メールアドレス",
        password: "パスワード",
        username: "ユーザー名",
        fullName: "フルネーム",
        postalCode: "郵便番号",
        loginButton: "あなたのキッチンに入る 👨‍🍳",
        registerButton: "コミュニティに参加",
        joinLambalia: "Lambaliaに参加"
      },

      cuisines: {
        american: "アメリカ料理",
        mexican: "メキシコ料理",
        italian: "イタリア料理",
        chinese: "中華料理", 
        indian: "インド料理",
        japanese: "日本料理",
        thai: "タイ料理",
        mediterranean: "地中海料理"
      }
    }
  },

  // Duplicate Arabic section removed - see complete Arabic section below

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
        filter: "تصفية",
        sort: "ترتيب",
        back: "رجوع",
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
        welcomeMessage: "انضم إلى مجتمعنا من الطهاة المنزليين الذين يشاركون الوصفات الأصيلة من جميع أنحاء العالم!"
      },

      home: {
        title: "لامباليا",
        subtitle: "حوّل مطبخك إلى تجربة طهي عالمية",
        welcomeMessage: "مرحباً بك في لامباليا - حيث تجد كل مطبخ ثقافي صوته",
        description: "تواصل مع الطهاة المنزليين الشغوفين، واكتشف الوصفات الأصيلة، وحوّل مطبخك إلى تجربة طهي عالمية.",
        features: {
          recipes: "198+ وصفة تقليدية",
          monetize: "استثمر مهاراتك في الطبخ",
          restaurant: "منصة المطعم المنزلي",
          communities: "80+ مجتمع ثقافي",
          heritageRecipes: "وصفات التراث",
          specialtyIngredients: "مكونات خاصة"
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
          description: "تعلم من أمهر الطهاة حول العالم",
          learnMore: "اعرف المزيد"
        },
        recipeSnippets: {
          title: "أحدث مقاطع الوصفات",
          subtitle: "نصائح طبخ سريعة من مجتمعنا",
          viewAll: "عرض جميع المقاطع",
          cookingTip: "نصيحة طبخ",
          noSnippets: "لم يتم العثور على مقاطع وصفات. كن أول من يشارك مقطع وصفتك التقليدية على لامباليا!"
        },
        communityStats: {
          title: "انضم إلى مجتمعنا الطهي العالمي",
          activeChefs: "الطهاة المنزليون النشطون",
          countriesServed: "البلدان المخدومة",
          recipesShared: "الوصفات المشتركة",
          culturesRepresented: "الثقافات الممثلة"
        }
      },

      // Forms
      forms: {
        createSnippet: {
          title: "إنشاء مقطع وصفة",
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