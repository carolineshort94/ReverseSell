import React from 'react';
import "../style/RequestCard.css";

const RequestCard = ({ request, isLoggedIn, onOfferClick }) => {
    return (
        <div className='request-card border rounded-lg p-4 shadow-sm bg-white mb-4'>
            <h2 className='text-lg font-semibold text-gray-800'>{request.title}</h2>
            <p className='text-sm text-gray-600 m-2'>{request.description}</p>
            <div className='text-sm text-gray-700 mb-1'>Budget: ${request.budget}</div>
            <div className='text-sm text-gray-700 mb-3'>Deadline: {request.deadline}</div>
            <button
                className='px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700'
                onClick={() => onOfferClick(request)}
            >
                {isLoggedIn ? "Make Offer" : "Login to Make an Offer"}
            </button>
        </div>
    )

}
export default RequestCard;
