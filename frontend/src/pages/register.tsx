import { Container, Box } from "@mui/material";
import RegisterForm from "../components/registerForm";

export function Register() {
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
                <RegisterForm />
            </Container>
        </Box>
    );
}
