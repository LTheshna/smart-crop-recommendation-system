import { useState } from "react";
import RecommendationCard from "./RecommendationCard";
import { predictCrop } from "../services/api";

function CropForm() {
  const [showAdvanced, setShowAdvanced] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [results, setResults] = useState([]);
  const [validationError, setValidationError] = useState("");

  const [formData, setFormData] = useState({
    region: "",
    soil_texture: "",
    season: "",
    temperature: "",
    humidity: "",
    rainfall: "",
    N: "",
    P: "",
    K: "",
    ph: "",
    moisture: "",
    historical_yield: "",
    market_price: "",
  });

  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  const validateForm = () => {
    if (!formData.region || !formData.soil_texture || !formData.season) {
      return "Please complete all required dropdown fields.";
    }

    if (
      formData.temperature === "" ||
      formData.humidity === "" ||
      formData.rainfall === ""
    ) {
      return "Temperature, humidity, and rainfall are required.";
    }

    if (formData.temperature < 5 || formData.temperature > 50) {
      return "Temperature must be between 5°C and 50°C.";
    }

    if (formData.humidity < 0 || formData.humidity > 100) {
      return "Humidity must be between 0% and 100%.";
    }

    if (formData.rainfall < 0 || formData.rainfall > 3000) {
      return "Rainfall must be between 0 and 3000 mm.";
    }

    return null;
  };

  const handleSubmit = async () => {
    const validationMessage = validateForm();

    if (validationMessage) {
      setValidationError(validationMessage);
      setResults([]);
      return;
    }

    setValidationError("");

    try {
      setLoading(true);
      setError("");

      const cleanedData = Object.fromEntries(
        Object.entries(formData).map(([key, value]) => [
          key,
          value === "" ? null : value,
        ])
      );

      const response = await predictCrop(cleanedData);

      setResults(response.recommendations || []);
    } catch (err) {
      setError("Failed to fetch recommendations.");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <div className="grid md:grid-cols-2 gap-4">
        <select
          name="region"
          onChange={handleChange}
          className="border rounded-lg p-3"
        >
          <option value="">Select Region</option>
          <option value="Andhra Pradesh">Andhra Pradesh</option>
          <option value="Arunachal Pradesh">Arunachal Pradesh</option>
          <option value="Assam">Assam</option>
          <option value="Bihar">Bihar</option>
          <option value="Chhattisgarh">Chhattisgarh</option>
          <option value="Goa">Goa</option>
          <option value="Gujarat">Gujarat</option>
          <option value="Haryana">Haryana</option>
          <option value="Himachal Pradesh">Himachal Pradesh</option>
          <option value="Jharkhand">Jharkhand</option>
          <option value="Karnataka">Karnataka</option>
          <option value="Kerala">Kerala</option>
          <option value="Madhya Pradesh">Madhya Pradesh</option>
          <option value="Maharashtra">Maharashtra</option>
          <option value="Manipur">Manipur</option>
          <option value="Meghalaya">Meghalaya</option>
          <option value="Mizoram">Mizoram</option>
          <option value="Nagaland">Nagaland</option>
          <option value="Odisha">Odisha</option>
          <option value="Punjab">Punjab</option>
          <option value="Rajasthan">Rajasthan</option>
          <option value="Sikkim">Sikkim</option>
          <option value="Tamil Nadu">Tamil Nadu</option>
          <option value="Telangana">Telangana</option>
          <option value="Tripura">Tripura</option>
          <option value="Uttar Pradesh">Uttar Pradesh</option>
          <option value="Uttarakhand">Uttarakhand</option>
          <option value="West Bengal">West Bengal</option>
        </select>

        <select
          name="soil_texture"
          onChange={handleChange}
          className="border rounded-lg p-3"
        >
          <option value="">Select Soil Texture</option>
          <option value="Clay">Clay</option>
          <option value="Clayey">Clayey</option>
          <option value="Loamy">Loamy</option>
          <option value="Sandy">Sandy</option>
          <option value="Silty">Silty</option>
        </select>

        <select
          name="season"
          onChange={handleChange}
          className="border rounded-lg p-3"
        >
          <option value="">Select Season</option>
          <option value="Summer">Summer</option>
          <option value="Monsoon">Monsoon</option>
          <option value="Winter">Winter</option>
        </select>

        <input
          name="temperature"
          type="number"
          placeholder="Temperature (°C)"
          onChange={handleChange}
          className="border rounded-lg p-3"
        />

        <input
          name="humidity"
          type="number"
          placeholder="Humidity (%)"
          onChange={handleChange}
          className="border rounded-lg p-3"
        />

        <input
          name="rainfall"
          type="number"
          placeholder="Rainfall (mm)"
          onChange={handleChange}
          className="border rounded-lg p-3"
        />
      </div>

      <button
        type="button"
        onClick={() => setShowAdvanced(!showAdvanced)}
        className="mt-4 text-green-700 font-semibold"
      >
        {showAdvanced ? "Hide Advanced Inputs ▲" : "Show Advanced Inputs ▼"}
      </button>

      {showAdvanced && (
        <div className="grid md:grid-cols-2 gap-4 mt-4">
          <input name="N" placeholder="Nitrogen" onChange={handleChange} className="border rounded-lg p-3" />
          <input name="P" placeholder="Phosphorus" onChange={handleChange} className="border rounded-lg p-3" />
          <input name="K" placeholder="Potassium" onChange={handleChange} className="border rounded-lg p-3" />
          <input name="ph" placeholder="pH" onChange={handleChange} className="border rounded-lg p-3" />
          <input name="moisture" placeholder="Moisture" onChange={handleChange} className="border rounded-lg p-3" />
          <input name="historical_yield" placeholder="Historical Yield" onChange={handleChange} className="border rounded-lg p-3" />
          <input name="market_price" placeholder="Market Price" onChange={handleChange} className="border rounded-lg p-3" />
        </div>
      )}

      {validationError && (
        <div className="mt-4 bg-red-50 border border-red-200 text-red-700 p-3 rounded-lg">
          {validationError}
        </div>
      )}

      <button
        onClick={handleSubmit}
        disabled={loading}
        className="mt-6 bg-green-700 text-white px-6 py-3 rounded-lg hover:bg-green-800 transition disabled:bg-gray-400"
      >
        {loading ? "Predicting..." : "Predict Best Crop"}
      </button>

      {error && (
        <p className="text-red-500 mt-4">{error}</p>
      )}

      {results.length > 0 && (
        <div className="mt-8">
          <h3 className="text-xl font-semibold mb-4 text-green-700">
            Recommended Crops
          </h3>

          <div className="grid md:grid-cols-2 gap-4">
            {results.map((rec, index) => (
              <RecommendationCard
                key={index}
                recommendation={rec}
                rank={index + 1}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default CropForm;