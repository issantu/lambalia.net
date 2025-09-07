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
        lod: "Local Offers & Demands",
        lodShort: "LOD",
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
        info: "Information",
        welcome: "Welcome",
        aiCook: "AI Cook",
        update: "Update",
        postOffer: "Post Offer",
        postDemand: "Post Demand",
        creating: "Creating...",
        saving: "Saving...",
        loadingData: "Loading data..."
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
        phoneNumber: "Phone Number",
        postalCode: "Postal Code",
        forgotPassword: "Forgot Password?",
        rememberMe: "Remember Me",
        loginButton: "Enter Your Kitchen 👨‍🍳",
        registerButton: "Start Your Culinary Journey",
        joinLambalia: "Join Lambalia",
        welcomeMessage: "Join our community of home chefs sharing authentic recipes from around the world!",
        phoneRequired: "Required for account security and order notifications",
        twoFactorTitle: "Enable Two-Layer Security (Recommended)",
        twoFactorDesc: "Add an extra layer of security to your account with SMS verification. This helps protect your earnings and personal information.",
        twoFactorFeatures: "SMS verification codes • Enhanced account protection • Secure payments",
        subtitle: "Taste the World's Heritage",
        culturalInfo: "🌍 80+ Cultural Communities • 🥄 Heritage Recipes • 🛒 Specialty Ingredients",
        nativeDishesLabel: "What native dishes from your culture can you cook? (This helps users find and pay you for authentic recipes)",
        consultationLabel: "What would you like other users to contact you for? (Paid consultations - you set your rates!)",
        culturalBgLabel: "Your Cultural Background (helps us connect you with the right community)"
      },

      // Home
      home: {
        title: "Lambalia",
        subtitle: "Transform Your Kitchen Into a Global Culinary Experience",
        features: {
          recipes: "198+ Traditional Recipes",
          monetize: "Monetize Your Cooking",
          restaurant: "Home Restaurant Platform"
        },
        actions: {
          browseName: "📚 Browse Templates",
          createName: "✨ Create Snippet", 
          ingredientsName: "🛒 Find Ingredients",
          restaurantName: "🏠👩‍🍳 Open Kitchen",
          marketplaceName: "🌱🛒 Local Market",
          charityName: "🤝❤️ Give Back",
          eatsName: "🚚🍽️ Quick Eats"
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

      // Local Offers & Demands (LOD)
      lod: {
        title: "Local Offers & Demands",
        subtitle: "Geo-Localized Food Marketplace (Lamba LOD)",
        description: "Connect local food offers and demands in your area • 15% commission",
        showingResults: "Showing results for:",
        availableOffers: "Available Offers",
        foodDemands: "Food Demands",
        availableFood: "Available Food Offers Near You",
        demandsInArea: "Food Demands in Your Area",
        noOffers: "No offers available in your area. Be the first to post one!",
        noDemands: "No demands in your area. Check back later!",
        filterLocation: "Filter by Location:",
        zipPlaceholder: "Enter zip code or postal code",
        loadingMarket: "Loading market data...",
        postOfferModal: "Post Food Offer",
        postDemandModal: "Post Food Demand",
        available: "Available",
        wanted: "Wanted",
        locked: "Locked",
        people: "people",
        prep: "prep",
        person: "person",
        pickup: "Pickup",
        delivery: "Delivery",
        timeLeft: "left",
        expired: "Expired",
        subscribeBuy: "Subscribe & Buy",
        canMake: "I Can Make This",
        title_: "Title",
        dishName: "Dish Name",
        description_: "Description",
        cuisineType: "Cuisine Type",
        quantity: "Quantity (People)",
        pricePerPerson: "Price per Person ($)",
        postalCode_: "Your Postal Code",
        prepTime: "Preparation Time (hours)",
        fulfillmentOptions: "Fulfillment Options",
        pickupAvailable: "Pickup Available",
        deliveryAvailable: "Delivery Available",
        spiceLevel: "Spice Level",
        mild: "Mild",
        medium: "Medium",
        hot: "Hot",
        veryHot: "Very Hot",
        commissionInfo: "Commission Info",
        commissionDesc: "Lambalia charges a 15% commission on all transactions.",
        earningsCalc: "You'll receive",
        fromTransaction: "from a",
        transaction: "transaction",
        titlePlaceholderOffer: "e.g., Fresh Jollof Rice Available",
        titlePlaceholderDemand: "e.g., Looking for Authentic Poulet Mayo",
        dishPlaceholder: "e.g., Jollof Rice with Chicken",
        descPlaceholder: "Describe the dish, ingredients, preparation style...",
        cuisinePlaceholder: "e.g., Nigerian, Thai, French",
        postalPlaceholder: "e.g., 90210 or SW1A 1AA",
        subscribeSuccess: "Successfully subscribed to",
        contactDetails: "You will be contacted with pickup/delivery details.",
        subscribeError: "Subscription failed. Please try again.",
        createSuccess: "created successfully!",
        createError: "Failed to create item. Please try again.",
        miles: "miles away",
        hours: "h",
        minutes: "m"
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
        lod: "Ofertas y Demandas Locales",
        lodShort: "ODL",
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
        welcome: "Bienvenido",
        aiCook: "Chef IA",
        update: "Actualizar",
        postOffer: "Publicar Oferta",
        postDemand: "Publicar Demanda",
        creating: "Creando...",
        saving: "Guardando...",
        loadingData: "Cargando datos..."
      },

      auth: {
        login: "Iniciar Sesión",
        register: "Registrarse",
        logout: "Cerrar Sesión",
        email: "Correo Electrónico",
        password: "Contraseña",
        username: "Nombre de Usuario",
        fullName: "Nombre Completo",
        phoneNumber: "Número de Teléfono",
        postalCode: "Código Postal",
        forgotPassword: "¿Olvidaste tu contraseña?",
        rememberMe: "Recordarme",
        loginButton: "Entra a Tu Cocina 👨‍🍳",
        registerButton: "Comienza Tu Viaje Culinario",
        joinLambalia: "Únete a Lambalia",
        welcomeMessage: "¡Únete a nuestra comunidad de chefs caseros compartiendo recetas auténticas de todo el mundo!",
        phoneRequired: "Requerido para seguridad de cuenta y notificaciones de pedidos",
        twoFactorTitle: "Habilitar Seguridad de Dos Capas (Recomendado)",
        twoFactorDesc: "Añade una capa extra de seguridad a tu cuenta con verificación SMS. Esto ayuda a proteger tus ganancias e información personal.",
        twoFactorFeatures: "Códigos de verificación SMS • Protección mejorada de cuenta • Pagos seguros"
      },

      home: {
        title: "Lambalia",
        subtitle: "Transforma Tu Cocina en una Experiencia Culinaria Global",
        features: {
          recipes: "198+ Recetas Tradicionales",
          monetize: "Monetiza Tu Cocina",
          restaurant: "Plataforma de Restaurante Casero"
        },
        actions: {
          browseName: "📚 Explorar Plantillas",
          createName: "✨ Crear Fragmento",
          ingredientsName: "🛒 Encontrar Ingredientes", 
          restaurantName: "🏠👩‍🍳 Abrir Cocina",
          marketplaceName: "🌱🛒 Mercado Local",
          charityName: "🤝❤️ Retribuir",
          eatsName: "🚚🍽️ Comida Rápida"
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
        lod: "Offres et Demandes Locales",
        lodShort: "ODL",
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
        phoneNumber: "Numéro de Téléphone",
        postalCode: "Code postal",
        forgotPassword: "Mot de passe oublié?",
        rememberMe: "Se souvenir de moi",
        loginButton: "Entrez dans Votre Cuisine 👨‍🍳",
        registerButton: "Commencez Votre Voyage Culinaire",
        joinLambalia: "Rejoindre Lambalia",
        welcomeMessage: "Rejoignez notre communauté de chefs à domicile partageant des recettes authentiques du monde entier!",
        phoneRequired: "Requis pour la sécurité du compte et les notifications de commande",
        twoFactorTitle: "Activer la Sécurité à Deux Couches (Recommandé)",
        twoFactorDesc: "Ajoutez une couche supplémentaire de sécurité à votre compte avec la vérification SMS. Cela aide à protéger vos gains et informations personnelles.",
        twoFactorFeatures: "Codes de vérification SMS • Protection de compte améliorée • Paiements sécurisés"
      },

      home: {
        title: "Lambalia", 
        subtitle: "Transformez Votre Cuisine en une Expérience Culinaire Mondiale",
        features: {
          recipes: "198+ Recettes Traditionnelles",
          monetize: "Monétisez Votre Cuisine",
          restaurant: "Plateforme de Restaurant à Domicile"
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
        lod: "Lokale Angebote & Nachfragen",
        lodShort: "LAN",
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
        phoneNumber: "Telefonnummer",
        postalCode: "Postleitzahl",
        forgotPassword: "Passwort vergessen?",
        rememberMe: "Angemeldet bleiben",
        loginButton: "Betreten Sie Ihre Küche 👨‍🍳",
        registerButton: "Beginnen Sie Ihre Kulinarische Reise",
        joinLambalia: "Lambalia Beitreten",
        welcomeMessage: "Treten Sie unserer Gemeinschaft von Hausköchen bei, die authentische Rezepte aus aller Welt teilen!",
        phoneRequired: "Erforderlich für Kontosicherheit und Bestellbenachrichtigungen",
        twoFactorTitle: "Zwei-Schicht-Sicherheit Aktivieren (Empfohlen)",
        twoFactorDesc: "Fügen Sie eine zusätzliche Sicherheitsschicht zu Ihrem Konto mit SMS-Verifizierung hinzu. Dies hilft, Ihre Einnahmen und persönlichen Informationen zu schützen.",
        twoFactorFeatures: "SMS-Verifizierungscodes • Erweiterte Kontosicherheit • Sichere Zahlungen"
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
        lod: "本地供需",
        lodShort: "供需",
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
        phoneNumber: "电话号码",
        postalCode: "邮政编码",
        forgotPassword: "忘记密码？",
        rememberMe: "记住我",
        loginButton: "进入您的厨房 👨‍🍳",
        registerButton: "开始您的烹饪之旅",
        joinLambalia: "加入Lambalia",
        welcomeMessage: "加入我们的家庭厨师社区，分享来自世界各地的正宗食谱！",
        phoneRequired: "账户安全和订单通知必需",
        twoFactorTitle: "启用双重安全验证（推荐）",
        twoFactorDesc: "通过短信验证为您的账户添加额外的安全层。这有助于保护您的收入和个人信息。",
        twoFactorFeatures: "短信验证码 • 增强账户保护 • 安全支付"
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
        lod: "地域オファー＆デマンド",
        lodShort: "LOD",
        profile: "プロフィール"
      },

      auth: {
        login: "ログイン",
        register: "登録",
        logout: "ログアウト",
        email: "メール",
        password: "パスワード",
        username: "ユーザー名",
        fullName: "氏名",
        phoneNumber: "電話番号",
        postalCode: "郵便番号",
        forgotPassword: "パスワードを忘れた？",
        rememberMe: "ログイン状態を保持",
        loginButton: "キッチンに入る 👨‍🍳",
        registerButton: "料理の旅を始める",
        joinLambalia: "Lambaliaに参加",
        welcomeMessage: "世界中の本格的なレシピを共有するホームシェフのコミュニティにご参加ください！",
        phoneRequired: "アカウントセキュリティと注文通知に必要",
        twoFactorTitle: "二段階認証を有効にする（推奨）",
        twoFactorDesc: "SMS認証でアカウントに追加のセキュリティ層を追加します。これにより収入と個人情報が保護されます。",
        twoFactorFeatures: "SMS認証コード • 強化されたアカウント保護 • 安全な支払い"
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

  ar: {
    translation: {
      nav: {
        browse: "تصفح القوالب",
        create: "إنشاء مقطع",
        ingredients: "العثور على المكونات", 
        restaurant: "فتح المطبخ",
        marketplace: "السوق المحلي",
        charity: "رد الجميل",
        eats: "الطعام السريع",
        lod: "العروض والطلبات المحلية",
        lodShort: "ع.ط",
        profile: "الملف الشخصي"
      },

      auth: {
        login: "دخول",
        register: "تسجيل",
        logout: "خروج",
        email: "البريد الإلكتروني",
        password: "كلمة المرور",
        username: "اسم المستخدم",
        fullName: "الاسم الكامل",
        phoneNumber: "رقم الهاتف",
        postalCode: "الرمز البريدي",
        forgotPassword: "نسيت كلمة المرور؟",
        rememberMe: "تذكرني",
        loginButton: "ادخل إلى مطبخك 👨‍🍳",
        registerButton: "ابدأ رحلتك الطهوية",
        joinLambalia: "انضم إلى Lambalia",
        welcomeMessage: "انضم إلى مجتمعنا من الطهاة المنزليين الذين يشاركون الوصفات الأصيلة من جميع أنحاء العالم!",
        phoneRequired: "مطلوب لأمان الحساب وإشعارات الطلبات",
        twoFactorTitle: "تفعيل الأمان ثنائي الطبقات (موصى به)",
        twoFactorDesc: "أضف طبقة إضافية من الأمان لحسابك مع التحقق عبر الرسائل النصية. هذا يساعد في حماية أرباحك ومعلوماتك الشخصية.",
        twoFactorFeatures: "رموز التحقق عبر الرسائل النصية • حماية محسنة للحساب • مدفوعات آمنة"
      },

      cuisines: {
        american: "أمريكي",
        mexican: "مكسيكي",
        italian: "إيطالي",
        chinese: "صيني",
        indian: "هندي",
        japanese: "ياباني", 
        thai: "تايلاندي",
        mediterranean: "متوسطي",
        middleEastern: "شرق أوسطي"
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
        lod: "Ofertas e Demandas Locais",
        lodShort: "ODL",
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
        phoneNumber: "Número de Telefone",
        postalCode: "CEP",
        forgotPassword: "Esqueceu a senha?",
        rememberMe: "Lembrar de mim",
        loginButton: "Entre na Sua Cozinha 👨‍🍳",
        registerButton: "Comece Sua Jornada Culinária",
        joinLambalia: "Junte-se à Lambalia",
        welcomeMessage: "Junte-se à nossa comunidade de chefs caseiros compartilhando receitas autênticas de todo o mundo!",
        phoneRequired: "Necessário para segurança da conta e notificações de pedidos",
        twoFactorTitle: "Ativar Segurança de Duas Camadas (Recomendado)",
        twoFactorDesc: "Adicione uma camada extra de segurança à sua conta com verificação por SMS. Isso ajuda a proteger seus ganhos e informações pessoais.",
        twoFactorFeatures: "Códigos de verificação SMS • Proteção aprimorada da conta • Pagamentos seguros"
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
        lod: "Местные Предложения и Запросы",
        lodShort: "МПЗ",
        profile: "Профиль"
      },

      auth: {
        login: "Войти",
        register: "Регистрация",
        logout: "Выйти",
        email: "Email",
        password: "Пароль",
        username: "Имя пользователя",
        fullName: "Полное имя",
        phoneNumber: "Номер Телефона",
        postalCode: "Почтовый индекс",
        forgotPassword: "Забыли пароль?",
        rememberMe: "Запомнить меня",
        loginButton: "Войти в Кухню 👨‍🍳",
        registerButton: "Начать Кулинарное Путешествие",
        joinLambalia: "Присоединиться к Lambalia",
        welcomeMessage: "Присоединяйтесь к нашему сообществу домашних поваров, делящихся аутентичными рецептами со всего мира!",
        phoneRequired: "Необходимо для безопасности аккаунта и уведомлений о заказах",
        twoFactorTitle: "Включить Двухуровневую Безопасность (Рекомендуется)",
        twoFactorDesc: "Добавьте дополнительный уровень безопасности в ваш аккаунт с SMS-верификацией. Это помогает защитить ваши доходы и личную информацию.",
        twoFactorFeatures: "SMS-коды верификации • Улучшенная защита аккаунта • Безопасные платежи"
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
        lod: "Offerte e Richieste Locali",
        lodShort: "ORL",
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
        phoneNumber: "Numero di Telefono",
        postalCode: "Codice postale",
        forgotPassword: "Password dimenticata?",
        rememberMe: "Ricordami",
        loginButton: "Entra nella Tua Cucina 👨‍🍳",
        registerButton: "Inizia il Tuo Viaggio Culinario",
        joinLambalia: "Unisciti a Lambalia",
        welcomeMessage: "Unisciti alla nostra comunità di chef casalinghi che condividono ricette autentiche da tutto il mondo!",
        phoneRequired: "Richiesto per la sicurezza dell'account e le notifiche degli ordini",
        twoFactorTitle: "Abilita Sicurezza a Due Livelli (Raccomandato)",
        twoFactorDesc: "Aggiungi un livello extra di sicurezza al tuo account con la verifica SMS. Questo aiuta a proteggere i tuoi guadagni e le informazioni personali.",
        twoFactorFeatures: "Codici di verifica SMS • Protezione account migliorata • Pagamenti sicuri"
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