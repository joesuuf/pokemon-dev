import React from 'react';
import { PokemonCard } from '../types/pokemon';

interface CardDisplayProps {
  card: PokemonCard;
}

// PERF-01: Memoize CardDisplay component to prevent unnecessary re-renders
export const CardDisplay = React.memo<CardDisplayProps>(({ card }) => {
  return (
    <div className="card-display-3col">
      <div className="card-display-header">
        <h2 className="card-name">{card.name}</h2>
        <p className="card-supertype">{card.supertype}</p>
      </div>

      <div className="card-display-grid">
        {/* COLUMN 1: Card Image */}
        <div className="card-col-1">
          <div className="card-image-container">
            <img
              src={card.images.large}
              alt={card.name}
              className="card-image-large"
              loading="lazy"
              onError={(e) => {
                (e.target as HTMLImageElement).src = card.images.small;
              }}
            />
          </div>
          <div className="card-specs">
            {card.hp && <p><strong>HP:</strong> {card.hp}</p>}
            {card.types && <p><strong>Types:</strong> {card.types.join(', ')}</p>}
            {card.subtypes && (
              <p><strong>Subtypes:</strong> {card.subtypes.join(', ')}</p>
            )}
            {card.rarity && <p><strong>Rarity:</strong> {card.rarity}</p>}
          </div>
        </div>

        {/* COLUMN 2: Set Info & Prices */}
        <div className="card-col-2">
          <div className="set-info">
            <h3>Set Information</h3>
            <p><strong>Set:</strong> {card.set.name}</p>
            <p><strong>Series:</strong> {card.set.series}</p>
            <p><strong>Number:</strong> {card.number}</p>
            <p><strong>Artist:</strong> {card.artist}</p>
            <p><strong>Release Date:</strong> {card.set.releaseDate}</p>
          </div>

          {card.tcgplayer && (
            <div className="pricing">
              <h3>TCGPlayer Prices</h3>
              {card.tcgplayer.prices.normal && (
                <div className="price-section">
                  <h4>Normal</h4>
                  <p>Low: ${card.tcgplayer.prices.normal.low}</p>
                  <p>Mid: ${card.tcgplayer.prices.normal.mid}</p>
                  <p>High: ${card.tcgplayer.prices.normal.high}</p>
                  <p>Market: ${card.tcgplayer.prices.normal.market}</p>
                </div>
              )}
              {card.tcgplayer.prices.holofoil && (
                <div className="price-section">
                  <h4>Holofoil</h4>
                  <p>Low: ${card.tcgplayer.prices.holofoil.low}</p>
                  <p>Mid: ${card.tcgplayer.prices.holofoil.mid}</p>
                  <p>High: ${card.tcgplayer.prices.holofoil.high}</p>
                  <p>Market: ${card.tcgplayer.prices.holofoil.market}</p>
                </div>
              )}
            </div>
          )}
        </div>

        {/* COLUMN 3: Specs/Attacks/etc */}
        <div className="card-col-3">
          {card.abilities && card.abilities.length > 0 && (
            <div className="abilities">
              <h3>Abilities</h3>
              {card.abilities.map((ability, index) => (
                <div key={index} className="ability">
                  <strong>{ability.name}</strong> ({ability.type})
                  <p>{ability.text}</p>
                </div>
              ))}
            </div>
          )}

          {card.attacks && card.attacks.length > 0 && (
            <div className="attacks">
              <h3>Attacks</h3>
              {card.attacks.map((attack, index) => (
                <div key={index} className="attack">
                  <div className="attack-header">
                    <strong>{attack.name}</strong>
                    <span className="attack-cost">
                      Cost: {attack.cost.join(', ')} ({attack.convertedEnergyCost})
                    </span>
                    <span className="attack-damage">Damage: {attack.damage}</span>
                  </div>
                  {attack.text && <p>{attack.text}</p>}
                </div>
              ))}
            </div>
          )}

          {card.weaknesses && card.weaknesses.length > 0 && (
            <div className="weaknesses">
              <h3>Weaknesses</h3>
              {card.weaknesses.map((weakness, index) => (
                <p key={index}>{weakness.type}: {weakness.value}</p>
              ))}
            </div>
          )}

          {card.resistances && card.resistances.length > 0 && (
            <div className="resistances">
              <h3>Resistances</h3>
              {card.resistances.map((resistance, index) => (
                <p key={index}>{resistance.type}: {resistance.value}</p>
              ))}
            </div>
          )}

          {card.retreatCost && (
            <div className="retreat">
              <h3>Retreat Cost</h3>
              <p>{card.retreatCost.join(', ')} ({card.convertedRetreatCost})</p>
            </div>
          )}

          {card.flavorText && (
            <div className="flavor-text">
              <p><em>{card.flavorText}</em></p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
});