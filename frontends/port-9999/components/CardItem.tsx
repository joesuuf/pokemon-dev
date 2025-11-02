import { Card } from '../types'

interface CardItemProps {
  card: Card
}

export default function CardItem({ card }: CardItemProps) {
  return (
    <div className="card-item">
      {/* Card Image */}
      <div className="card-item-image">
        {card.image && (
          <img
            src={card.image}
            alt={card.name}
            onError={(e) => {
              (e.target as HTMLImageElement).src =
                'https://via.placeholder.com/200x280?text=Card+Not+Found'
            }}
          />
        )}
      </div>

      {/* Card Info */}
      <div className="card-item-content">
        <h3 className="card-item-title">{card.name}</h3>
        <p className="card-item-meta">
          {card.set} #{card.cardNumber}
        </p>

        {/* Prices */}
        <div className="card-item-prices">
          {card.prices.usd && (
            <div className="price-row">
              <span className="price-label">USD:</span>
              <span className="price-value">${card.prices.usd.toFixed(2)}</span>
            </div>
          )}
          {card.prices.usdFoil && (
            <div className="price-row">
              <span className="price-label">Foil USD:</span>
              <span className="price-value">${card.prices.usdFoil.toFixed(2)}</span>
            </div>
          )}
          {card.prices.eur && (
            <div className="price-row">
              <span className="price-label">EUR:</span>
              <span className="price-value">€{card.prices.eur.toFixed(2)}</span>
            </div>
          )}
          {!card.prices.usd && !card.prices.usdFoil && !card.prices.eur && (
            <p className="text-gray-400 italic text-sm">Price data unavailable</p>
          )}
        </div>

        {/* Links */}
        <div className="card-item-links">
          {card.links.tcgplayer && (
            <a
              href={card.links.tcgplayer}
              target="_blank"
              rel="noopener noreferrer"
              className="tcgplayer-btn"
            >
              TCGPlayer
            </a>
          )}
          {card.links.cardmarket && (
            <a
              href={card.links.cardmarket}
              target="_blank"
              rel="noopener noreferrer"
              className="cardmarket-btn"
            >
              Cardmarket
            </a>
          )}
        </div>
      </div>
    </div>
  )
}
