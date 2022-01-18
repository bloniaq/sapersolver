class NegativeMinesLeftCountError(Exception):

    def __init__(self, field, board):
        message = f"Mines count out of range\n" \
                  f"{field}\n" \
                  f"Mines in neighbourhood = {len(field.get_nbours('m', 'pm'))}" \
                  f": {field.get_nbours('m', 'pm')}\n" \
                  f"{field.state} - {len(field.get_nbours('m', 'pm'))} = " \
                  f"{int(field.state) - len(field.get_nbours('m', 'pm'))}\n" \
                  f"{board}"
        super().__init__(message)