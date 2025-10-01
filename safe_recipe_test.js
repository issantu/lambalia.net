// Quick fix for the React error - Add this to the top of RecipeTemplatesPage render
// This is a temporary hotfix while waiting for deployment

const RecipeTemplatesPage = () => {
  // ... existing state and functions ...

  // Add this safety function
  const renderSafeRecipeName = (recipe) => {
    if (typeof recipe === 'string') return recipe;
    if (recipe && typeof recipe === 'object') {
      return recipe.name_english || recipe.name || 'Unknown Recipe';
    }
    return 'Unknown Recipe';
  };

  // Update the render to use this safety function everywhere recipes are displayed
  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      {/* Add error boundary to catch and display any render errors */}
      {loading ? (
        <div className="flex justify-center items-center py-20">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-green-500"></div>
        </div>
      ) : (
        <div>
          {/* Success - show content */}
          <h1 className="text-3xl font-bold text-gray-900 mb-8">Browse Recipe Templates</h1>
          <p>Countries loaded: {countries.length}</p>
          <p>Recipe categories loaded: {Object.keys(nativeRecipes).length}</p>
          
          {/* Test render - show first few countries safely */}
          {Object.entries(nativeRecipes).slice(0, 3).map(([countryName, recipes]) => (
            <div key={countryName} className="mb-4 p-4 border">
              <h3>{countryName}</h3>
              <div>
                {Array.isArray(recipes) ? recipes.slice(0, 3).map((recipe, idx) => (
                  <span key={idx} className="mr-2">
                    {renderSafeRecipeName(recipe)}
                  </span>
                )) : 'No recipes'}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};