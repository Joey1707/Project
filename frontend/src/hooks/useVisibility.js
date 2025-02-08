import { useState } from "react";

function useVisibility(defaultValue) {
	const [visible, setVisible] = useState(defaultValue);

	const onVisibiltiyToggle = () => {
		setVisible(visible ? false : true);
	};

	return [visible, onVisibiltiyToggle];
}

export default useVisibility;
