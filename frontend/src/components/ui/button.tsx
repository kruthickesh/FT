import { cn } from "@/lib/utils";
import { Slot } from "@radix-ui/react-slot";
import { ButtonHTMLAttributes, forwardRef } from "react";

interface ButtonProps extends ButtonHTMLAttributes<HTMLButtonElement> { asChild?: boolean; variant?: "default" | "outline" | "ghost" | "destructive"; size?: "default" | "sm" | "lg" | "icon"; }

const Button = forwardRef<HTMLButtonElement, ButtonProps>(({ className, variant = "default", size = "default", asChild = false, ...props }, ref) => {
  const variants = { default: "bg-primary text-white hover:bg-primary/90", outline: "border border-gray-300 bg-white hover:bg-gray-50", ghost: "hover:bg-gray-100", destructive: "bg-red-500 text-white hover:bg-red-600" };
  const sizes = { default: "h-10 px-4 py-2", sm: "h-9 rounded-md px-3", lg: "h-11 rounded-md px-8", icon: "h-10 w-10" };
  const Comp = asChild ? Slot : "button";
  return <Comp className={cn("inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors disabled:opacity-50", variants[variant], sizes[size], className)} ref={ref} {...props} />;
});
Button.displayName = "Button";

export { Button };