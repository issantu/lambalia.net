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
        loginButton: "ادخل إلى مطبخك 👨‍🍳",
        registerButton: "انضم للمجتمع",
        joinLambalia: "انضم إلى لامباليا"
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