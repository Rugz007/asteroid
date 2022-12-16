import React, { useState } from "react";

interface PythonEditorProps
  extends React.TextareaHTMLAttributes<HTMLTextAreaElement> {
  highlightFunction: Function;
  onValueChange: Function;
  code: string;
}

const styles = {
  textarea: {
    top: 0,
    left: 0,
    height: "100%",
    width: "100%",
    color: "inherit",
    overflow: "hidden",
    MozOsxFontSmoothing: "grayscale",
    WebkitFontSmoothing: "antialiased",
    WebkitTextFillColor: "transparent",
  },
};

const PythonEditor: React.FC<PythonEditorProps> = ({
  highlightFunction,
  onValueChange,
  ...textAreaProps
}) => {
  const highlightedText = highlightFunction(textAreaProps.code);
  const [tempValue, setTempValue] = useState("");
  const handleChange = (e: any) => {
    onValueChange(e.target.value);
    e.target.value = "";
  };
  return (
    <>
      <pre dangerouslySetInnerHTML={{ __html: highlightedText }} />
      <textarea
        style={{ ...styles.textarea }}
        onChange={handleChange}
        {...textAreaProps}
      />
    </>
  );
};

export default PythonEditor;
