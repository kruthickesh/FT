"use client";
import { useState } from "react";
import { Star } from "lucide-react";
import { cn } from "@/lib/utils";

interface RatingProps {
  value: number;
  onChange?: (rating: number) => void;
  readonly?: boolean;
  size?: "sm" | "md" | "lg";
}

export function Rating({ value, onChange, readonly = false, size = "md" }: RatingProps) {
  const [hover, setHover] = useState(0);
  const sizes = { sm: 16, md: 20, lg: 24 };

  return (
    <div className="flex gap-1">
      {[1, 2, 3, 4, 5].map((star) => (
        <Star
          key={star}
          size={sizes[size]}
          className={cn("cursor-pointer transition-colors", !readonly && "hover:scale-110",
            star <= (hover || value) ? "text-yellow-500 fill-yellow-500" : "text-gray-300")}
          onMouseEnter={() => !readonly && setHover(star)}
          onMouseLeave={() => !readonly && setHover(0)}
          onClick={() => !readonly && onChange?.(star)}
        />
      ))}
    </div>
  );
}