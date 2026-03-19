import { Container, Box } from "@mui/material";
import LoginForm from "../components/loginForm";

export function Login() {
    return (
        <Box
            sx={{
                minHeight: "100vh",
                width: "100vw",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                bgcolor: "#f5f5f5",
            }}
        >
            <Container maxWidth="xs">
                <LoginForm />
            </Container>
        </Box>
    );
}
