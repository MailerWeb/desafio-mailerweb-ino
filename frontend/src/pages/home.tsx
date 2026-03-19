import { useEffect, useState } from "react";
import {
    Container,
    Typography,
    Box,
    SpeedDial,
    SpeedDialIcon,
    SpeedDialAction,
    Pagination,
    Stack,
} from "@mui/material";
import AssignmentIcon from "@mui/icons-material/Assignment";
import FolderIcon from "@mui/icons-material/Folder";
import TaskForm from "../components/taskForm";
import serviceAPI from "../services/mainService";
import type { Task, Category } from "../type/task";
import HeaderMenu from "../components/headerMenu";
import CategoryForm from "../components/categoryForm";
import FilterStatus from "../components/filterStatus";
import TasksList from "../components/tasksList";

const HomePage = () => {
    return (
        <Box
            sx={{
                display: "flex",
                flexDirection: "column",
                minHeight: "100vh",
                bgcolor: "#f5f5f5",
                margin: 0,
                padding: 0,
                overflowX: "hidden",
            }}
        >
            <HeaderMenu />
            <Container
                maxWidth="md"
                sx={{
                    mt: 4,
                    mb: 4,
                    flexGrow: 1,
                    pb: 10,
                }}
            >
                <Typography variant="h4" gutterBottom fontWeight="bold">
                    Minhas Reuniões
                </Typography>
            </Container>
        </Box>
    );
};

export default HomePage;
