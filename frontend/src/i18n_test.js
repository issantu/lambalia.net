// Test i18n configuration
import i18n from './i18n';

console.log('i18n configuration test:');
console.log('Available resources:', Object.keys(i18n.options.resources));
console.log('Current language:', i18n.language);
console.log('English auth.login:', i18n.getResource('en', 'translation', 'auth.login'));
console.log('Spanish auth.login:', i18n.getResource('es', 'translation', 'auth.login'));

// Test translation function
console.log('Translation test - en:', i18n.t('auth.login', { lng: 'en' }));
console.log('Translation test - es:', i18n.t('auth.login', { lng: 'es' }));