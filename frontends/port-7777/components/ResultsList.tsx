import { Card } from '../types'
import CardItem from './CardItem'

interface ResultsListProps {
  cards: Card[]
}

export default function ResultsList({ cards }: ResultsListProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {cards.map((card) => (
        <CardItem key={card.id} card={card} />
      ))}
    </div>
  )
}
