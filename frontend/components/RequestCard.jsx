import React from 'react';
import "../style/RequestCard.css";

const RequestCard = ({ request, isLoggedIn, onOfferClick }) => {
    return (
        <div className='request-card'>
            <h3 className='request-title'>{request.title}</h3>
            <p className='request-description'>{request.description}</p>

            <div className='tag-container'>
                {request.category && (
                    <span
                        key={request.category.name}
                        className={`tag-pill ${request.category.name.toLowerCase().replace(/[^a-z0-9]/g, '-')}`}>
                        {request.category.name}
                    </span>
                )}

            </div>

            <div className='card-footer'>
                <span className='expiry-date'> Expires in: {request.expiry_date}</span>
                <button
                    className='details-link'
                    onClick={() => onOfferClick(request)} >
                    View Details & Offers →
                </button>
            </div>
        </div>
    )

}
export default RequestCard;
