import Head from "next/head";
import Image from "next/image";
import { Inter } from "@next/font/google";
import styles from "../styles/Home.module.css";
import { Box, Button, Flex } from "@chakra-ui/react";
import Cell from "../components/Cell";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
  return (
    <>
      <Flex
        w="100%"
        flexDir={"column"}
        p="2%"
        backgroundColor={"gray.100"}
        h="100vh"
      >
        <Box bg="white" p="2%" borderRadius='lg'>
          <Cell />
          <Cell />
          <Cell />
        </Box>
      </Flex>
    </>
  );
}
