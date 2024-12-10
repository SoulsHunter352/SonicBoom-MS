export default function validate(rules, value) {
  console.log("Зашли");
  var errorMessage = "";
  if (!rules.required && value == "") {
    return errorMessage;
  }
  if (!value) {
    //setError("Обязательное поле");
    //console.log("Обязательное поле");
    errorMessage = "Обязательное поле";
  } else if (rules.minLength && value.length < rules.minLength) {
    errorMessage = "Минимальное количество символов " + rules.minLength;
    //setError("Минимальное количество символов " + input.minLength);
  } else if (rules.maxLength != -1 && value.length > rules.maxLength) {
    errorMessage = "Максимальное количество символов " + rules.maxLength;
    //setError("Максимальное количество символов " + input.maxLength);
  }
  return errorMessage;
}
