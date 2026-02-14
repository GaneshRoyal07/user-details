from pydantic import BaseModel, field_validator, ValidationError


class CreditCard(BaseModel):
    card_number: str

    # Validator for card number
    @field_validator("card_number")
    @classmethod
    def validate_card_number(cls, value):
        
        # Step 1: Remove spaces
        value = value.replace(" ", "")

        # Step 2: Check if only digits
        if not value.isdigit():
            raise ValueError("Card number must contain only digits")

        # Step 3: Check length
        if len(value) != 16:
            raise ValueError("Card number must be 16 digits")

        # Step 4: Apply Luhn Algorithm
        total = 0
        reverse_digits = value[::-1] #reverse the digits

        for i in range(len(reverse_digits)): #
            digit = int(reverse_digits[i]) 

            if i % 2 == 1: 
                digit *= 2   #double every second digit
                if digit > 9:
                    digit -= 9  #subtract 9 if greater than 9

            total += digit   #add all digits

        if total % 10 != 0:      #check divisible by 10
            raise ValueError("Invalid credit card number (Luhn check failed)")

        return value


# Testing
try:
    card = CreditCard(card_number="4539578763621486")
    print("✅ Valid Card:", card.card_number)

except ValidationError as e:
    print("❌ Validation Error")
    print(e)
