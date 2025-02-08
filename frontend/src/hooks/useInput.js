import { useState } from "react";

function useInput(InitialValue) {
	const [input, setInput] = useState(InitialValue);
	const handleValueCHange = (event) => setInput(event.target.value);
	return [input, handleValueCHange];
}

export default useInput;
