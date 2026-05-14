function RecommendationCard({ recommendation, rank }) {
    const confidence = recommendation.confidence || 0;
  
    return (
      <div className="bg-white border border-green-200 rounded-2xl p-6 shadow-md hover:shadow-lg transition">
        
        <div className="flex justify-between items-center mb-4">
          <h3 className="text-2xl font-bold text-green-800 capitalize">
            {recommendation.crop}
          </h3>
  
          <span className="bg-green-700 text-white text-sm px-3 py-1 rounded-full font-semibold">
            #{rank}
          </span>
        </div>
  
        <div className="mb-4">
          <div className="flex justify-between text-sm font-medium mb-1">
            <span>Confidence</span>
            <span>{confidence}%</span>
          </div>
  
          <div className="w-full bg-gray-200 rounded-full h-3">
            <div
              className="bg-green-600 h-3 rounded-full transition-all duration-500"
              style={{ width: `${confidence}%` }}
            />
          </div>
        </div>
  
        <div className="flex flex-wrap gap-2 mb-4">
          {recommendation.estimated_profit && (
            <span className="bg-blue-100 text-blue-800 text-sm px-3 py-1 rounded-full font-medium">
              ₹{recommendation.estimated_profit} Profit
            </span>
          )}
  
          {recommendation.combined_score && (
            <span className="bg-purple-100 text-purple-800 text-sm px-3 py-1 rounded-full font-medium">
              Score: {recommendation.combined_score}
            </span>
          )}
        </div>
  
        <p className="text-gray-600 text-sm leading-relaxed border-t pt-3">
          {recommendation.reason}
        </p>
      </div>
    );
  }
  
  export default RecommendationCard;