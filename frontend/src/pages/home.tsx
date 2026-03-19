import { Container, Typography, Box } from "@mui/material";
import HeaderMenu from "../components/headerMenu";

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
