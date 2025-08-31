// Professional SVG Icons Component - Replacing Emoji Icons
import React from 'react';

// Professional SVG Icons for Lambalia Platform
export const ProfessionalIcons = {
  // Navigation Icons
  Home: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
    </svg>
  ),

  Browse: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M4 6h16M4 12h16M4 18h16"/>
    </svg>
  ),

  Create: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 5v14m7-7H5"/>
    </svg>
  ),

  // Cooking & Food Icons
  ChefHat: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M6 2c1.1 0 2 .9 2 2v1c0 3.31 2.69 6 6 6s6-2.69 6-6V4c0-1.1.9-2 2-2s2 .9 2 2v1c0 4.42-3.58 8-8 8H8c-4.42 0-8-3.58-8-8V4c0-1.1.9-2 2-2z"/>
      <rect x="4" y="12" width="16" height="8" rx="2"/>
    </svg>
  ),

  Utensils: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M3 2v5c0 1.1.9 2 2 2h1v13h2V9h1c1.1 0 2-.9 2-2V2H3zM16 2v10c0 1.1.9 2 2 2s2-.9 2-2V2h-4z"/>
    </svg>
  ),

  Recipe: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
      <polyline points="14,2 14,8 20,8"/>
      <line x1="16" y1="13" x2="8" y2="13"/>
      <line x1="16" y1="17" x2="8" y2="17"/>
      <polyline points="10,9 9,9 8,9"/>
    </svg>
  ),

  // Restaurant & Marketplace Icons
  Restaurant: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M6 2c1.1 0 2 .9 2 2v1c0 3.31 2.69 6 6 6s6-2.69 6-6V4c0-1.1.9-2 2-2s2 .9 2 2v1c0 4.42-3.58 8-8 8H8c-4.42 0-8-3.58-8-8V4c0-1.1.9-2 2-2z"/>
      <rect x="2" y="12" width="20" height="8" rx="2"/>
      <circle cx="7" cy="16" r="1"/>
      <circle cx="12" cy="16" r="1"/>
      <circle cx="17" cy="16" r="1"/>
    </svg>
  ),

  Store: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M2 3h6l.4 2M7 13h10l4-8H5.4m-.4-2L4 3H2m5 10v6a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2v-6"/>
    </svg>
  ),

  Marketplace: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <rect x="2" y="3" width="20" height="14" rx="2" ry="2"/>
      <line x1="8" y1="21" x2="16" y2="21"/>
      <line x1="12" y1="17" x2="12" y2="21"/>
      <circle cx="8" cy="9" r="2"/>
      <circle cx="16" cy="9" r="2"/>
    </svg>
  ),

  // Smart Cooking Tool Icons
  SmartCooking: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
      <circle cx="12" cy="12" r="3"/>
      <path d="M12 1v6m0 6v6m11-7l-6 6m-6-6l-6-6"/>
    </svg>
  ),

  AI: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <circle cx="12" cy="12" r="3"/>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
  ),

  Ingredients: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M8 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2h4a1 1 0 0 1 1 1v14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V6a1 1 0 0 1 1-1h4V3z"/>
    </svg>
  ),

  // Heritage & Culture Icons
  Heritage: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <circle cx="12" cy="12" r="10"/>
      <line x1="2" y1="12" x2="22" y2="12"/>
      <path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/>
    </svg>
  ),

  Culture: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 2L2 7v10c0 5.55 3.84 9.74 9 9 5.16.74 9-3.45 9-9V7l-10-5z"/>
      <path d="M8 11l2 2 4-4"/>
    </svg>
  ),

  // Social & Community Icons
  Community: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"/>
      <circle cx="9" cy="7" r="4"/>
      <path d="M23 21v-2a4 4 0 0 0-3-3.87"/>
      <path d="M16 3.13a4 4 0 0 1 0 7.75"/>
    </svg>
  ),

  Heart: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/>
    </svg>
  ),

  // Farm & Eco Icons
  Farm: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="m12 2-3 3-3-3v6l3-3 3 3V2zM12 22l3-3 3 3v-6l-3 3-3-3v6z"/>
      <path d="M2 12l3 3 3-3H2zM22 12l-3-3-3 3h6z"/>
      <circle cx="12" cy="12" r="3"/>
    </svg>
  ),

  Leaf: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M17 8C8 10 5.9 16.17 3.82 21.34l1.58.66L8 15s4-2 8-2c4.37 0 8 3.63 8 8H2c0-4.37 3.63-8 8-8z"/>
    </svg>
  ),

  // Payment & Business Icons
  Payment: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <rect x="1" y="4" width="22" height="16" rx="2" ry="2"/>
      <line x1="1" y1="10" x2="23" y2="10"/>
    </svg>
  ),

  Dollar: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <line x1="12" y1="1" x2="12" y2="23"/>
      <path d="M17 5H9.5a3.5 3.5 0 0 0 0 7h5a3.5 3.5 0 0 1 0 7H6"/>
    </svg>
  ),

  // Settings & Profile Icons
  Settings: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <circle cx="12" cy="12" r="3"/>
      <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z"/>
    </svg>
  ),

  Profile: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M20 21v-2a4 4 0 0 0-4-4H8a4 4 0 0 0-4 4v2"/>
      <circle cx="12" cy="7" r="4"/>
    </svg>
  ),

  // Security Icons
  Shield: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
  ),

  Lock: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
      <circle cx="12" cy="16" r="1"/>
      <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
    </svg>
  ),

  // Navigation & Action Icons
  Search: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <circle cx="11" cy="11" r="8"/>
      <path d="m21 21-4.35-4.35"/>
    </svg>
  ),

  Filter: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <polygon points="22,3 2,3 10,12.46 10,19 14,21 14,12.46"/>
    </svg>
  ),

  Star: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/>
    </svg>
  ),

  ChevronRight: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <polyline points="9,18 15,12 9,6"/>
    </svg>
  ),

  ChevronDown: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <polyline points="6,9 12,15 18,9"/>
    </svg>
  ),

  // Communication Icons
  Message: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/>
    </svg>
  ),

  Phone: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/>
    </svg>
  ),

  Video: ({ size = 24, className = "" }) => (
    <svg width={size} height={size} className={className} viewBox="0 0 24 24" fill="currentColor">
      <polygon points="23,7 16,12 23,17"/>
      <rect x="1" y="5" width="15" height="14" rx="2" ry="2"/>
    </svg>
  )
};

// Icon wrapper component with consistent styling
export const Icon = ({ name, size = 24, className = "", color = "currentColor", ...props }) => {
  const IconComponent = ProfessionalIcons[name];
  
  if (!IconComponent) {
    console.warn(`Icon "${name}" not found`);
    return null;
  }
  
  return (
    <IconComponent 
      size={size} 
      className={`inline-block ${className}`}
      style={{ color }}
      {...props}
    />
  );
};

// Animated icon wrapper for special effects
export const AnimatedIcon = ({ name, size = 24, className = "", animation = "hover:scale-110", ...props }) => {
  return (
    <div className={`transition-transform duration-200 ${animation} ${className}`}>
      <Icon name={name} size={size} {...props} />
    </div>
  );
};

export default ProfessionalIcons;