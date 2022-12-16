import { Box, Input, Textarea } from "@chakra-ui/react";
import React, { useEffect, useState } from "react";
import { highlight, languages } from "../util/Prism";
import Editor from "react-simple-code-editor";
import "../styles/Cell.module.css";
import PythonEditor from "./Editor";
const styles = {
  color: "inherit",
  overflow: "hidden",
  MozOsxFontSmoothing: "grayscale",
  WebkitFontSmoothing: "antialiased",
  WebkitTextFillColor: "transparent",
  border: 0,
};
const Cell = () => {
  const [value, setValue] = useState("import test");
  const [renderValue, setRenderValue] = useState("");
  useEffect(() => {}, []);

  return (
    <Box w="100%" mb="2%" borderRadius={"xl"} display={"flex"}>
      <Editor
        value={value}
        onValueChange={setValue}
        //@ts-ignore
        highlight={(code) =>
          //@ts-ignore
          highlight(code, languages.python, "py")
        }
        className="dank"
        padding={10}
        style={{
          fontFamily: '"Fira code", "Fira Mono", monospace',
          fontSize: 14,
          width: "100%",
          borderRadius: "0.4rem",
          border: 0,
          backgroundColor: "#EDF2F7",
        }}
      />
      {/* <PythonEditor
        code={value}
        onValueChange={setValue}
        highlightFunction={(code: string) =>
          //@ts-ignore
          highlight(code, languages.python, "py")
        }
      /> */}
    </Box>
  );
};

export default Cell;
