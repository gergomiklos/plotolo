
export const valueFallback = (...values) => {
  for(let value of values) {
    if (value != null) {
      return value;
    }
  }
}