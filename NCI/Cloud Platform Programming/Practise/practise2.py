class WeightCalculator:
    @staticmethod
    def recommended_weight(age, height):
        return (height - 100 + age % 10) * 0.90

# --- Main Program ---
age = int(input("Enter your age: "))
height = float(input("Enter your height (cm): "))

rw = WeightCalculator.recommended_weight(age, height)
print(f"Your recommended weight is: {rw:.2f} kg")
