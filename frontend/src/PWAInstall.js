import React, { useState, useEffect } from 'react';

const PWAInstall = () => {
  const [deferredPrompt, setDeferredPrompt] = useState(null);
  const [showInstallButton, setShowInstallButton] = useState(false);

  useEffect(() => {
    // Register service worker
    if ('serviceWorker' in navigator) {
      window.addEventListener('load', () => {
        navigator.serviceWorker
          .register('/service-worker.js')
          .then((registration) => {
            console.log('✅ Service Worker registered:', registration.scope);
          })
          .catch((error) => {
            console.log('❌ Service Worker registration failed:', error);
          });
      });
    }

    // Listen for beforeinstallprompt event
    const handleBeforeInstallPrompt = (e) => {
      // Prevent the mini-infobar from appearing on mobile
      e.preventDefault();
      // Save the event so it can be triggered later
      setDeferredPrompt(e);
      // Show install button
      setShowInstallButton(true);
    };

    window.addEventListener('beforeinstallprompt', handleBeforeInstallPrompt);

    // Check if app is already installed
    if (window.matchMedia('(display-mode: standalone)').matches) {
      setShowInstallButton(false);
    }

    return () => {
      window.removeEventListener('beforeinstallprompt', handleBeforeInstallPrompt);
    };
  }, []);

  const handleInstallClick = async () => {
    if (!deferredPrompt) {
      return;
    }

    // Show the install prompt
    deferredPrompt.prompt();

    // Wait for the user to respond to the prompt
    const { outcome } = await deferredPrompt.userChoice;
    console.log(`User response to install prompt: ${outcome}`);

    // Clear the deferredPrompt so it can only be used once
    setDeferredPrompt(null);
    setShowInstallButton(false);
  };

  if (!showInstallButton) {
    return null;
  }

  return (
    <div className="fixed bottom-4 left-4 right-4 md:left-auto md:right-4 md:max-w-sm z-50">
      <div className="bg-gradient-to-r from-green-500 to-green-600 text-white rounded-lg shadow-2xl p-4 flex items-center justify-between animate-slide-up">
        <div className="flex-1">
          <p className="font-semibold text-sm">Install Lambalia App</p>
          <p className="text-xs opacity-90">Get quick access to recipes & cooking tools</p>
        </div>
        <div className="flex gap-2 ml-3">
          <button
            onClick={handleInstallClick}
            className="bg-white text-green-600 px-4 py-2 rounded-lg font-medium text-sm hover:bg-green-50 transition-colors"
          >
            Install
          </button>
          <button
            onClick={() => setShowInstallButton(false)}
            className="text-white hover:bg-white/20 px-2 rounded-lg transition-colors"
          >
            ✕
          </button>
        </div>
      </div>
    </div>
  );
};

export default PWAInstall;
