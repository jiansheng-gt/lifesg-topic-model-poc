import { CardItem } from "./card.styles";

interface CardProps {
  title: string;
  subtext?: string;
  onClick: () => void;
}

export const Card = ({ title, subtext, onClick }: CardProps) => {
  return (
    <CardItem onClick={onClick}>
      <h3>{title}</h3>
      {subtext && <body>{subtext}</body>}
    </CardItem>
  );
};
