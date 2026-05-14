import CropForm from "../components/CropForm";
function Home() {
    return (
      <div className="min-h-screen bg-green-50">
        {/* Header */}
        <header className="bg-green-700 text-white shadow-md">
          <div className="max-w-6xl mx-auto px-6 py-5">
            <h1 className="text-3xl font-bold">
              Smart Crop Recommendation System
            </h1>
            <p className="text-green-100 mt-1">
              AI-Powered Agricultural Decision Support Platform
            </p>
          </div>
        </header>
  
        {/* Main Content */}
        <main className="max-w-6xl mx-auto px-6 py-10">
  
          {/* Intro Card */}
          <section className="bg-white rounded-2xl shadow-md p-6 mb-8">
            <h2 className="text-2xl font-semibold text-green-700 mb-3">
              Crop Recommendation Prototype
            </h2>
            <p className="text-gray-600 leading-relaxed">
              Provide soil and environmental parameters to receive
              intelligent crop recommendations optimized for
              suitability, agronomic constraints, and profitability.
            </p>
          </section>
  
          {/* Input Form Placeholder */}
          <section className="bg-white rounded-2xl shadow-md p-6 mb-8">
            <h3 className="text-xl font-semibold text-gray-700 mb-2">
              Crop Input Form
            </h3>
            <CropForm />
          </section>
  
       
        </main>
      </div>
    );
  }
  
  export default Home;