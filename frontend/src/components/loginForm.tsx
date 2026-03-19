import { useState } from "react";
import { useAuth } from "../contexts/authContext";
import { useNavigate } from "react-router-dom";
import { Link as RouterLink } from "react-router-dom";
import {
    Box,
    TextField,
    Button,
    Typography,
    Paper,
    Alert,
    Link,
} from "@mui/material";

const LoginForm = () => {
    const [username_email, setUsernameEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState(false);

    const { login } = useAuth();
    const navigate = useNavigate();

    const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError(false);
        try {
            await login(username_email, password);
            navigate("/home");
        } catch (error) {
            setError(true);
            console.error("Erro na autenticação:", error);
        }
    };

    return (
        <Paper
            elevation={3}
            sx={{ p: 4, width: "100%", maxWidth: 400, borderRadius: 2 }}
        >
            <Paper elevation={3} sx={{ bgcolor: "#1976d2" }}>
                <Typography
                    variant="h4"
                    component="h1"
                    align="center"
                    gutterBottom
                    fontWeight="bold"
                    color="#ffffff"
                >
                    BOOKING APP MANAGER
                </Typography>
            </Paper>
            <Box component="form" onSubmit={handleSubmit} noValidate>
                <Typography
                    variant="h5"
                    component="h1"
                    align="center"
                    gutterBottom
                    fontWeight="bold"
                >
                    Login
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        E-mail/username ou senha incorretos.
                    </Alert>
                )}

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="E-mail/username"
                    value={username_email}
                    onChange={(e) => setUsernameEmail(e.target.value)}
                    autoComplete="email"
                    autoFocus
                    sx={{
                        "& input:-webkit-autofill": {
                            WebkitBoxShadow: "0 0 0 100px white inset",
                            WebkitTextFillColor: "#000",
                        },
                    }}
                />
                <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Senha"
                    type="password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    autoComplete="current-password"
                    sx={{
                        "& input:-webkit-autofill": {
                            WebkitBoxShadow: "0 0 0 100px white inset",
                            WebkitTextFillColor: "#000",
                        },
                    }}
                />
                <Button
                    type="submit"
                    fullWidth
                    variant="contained"
                    size="large"
                    sx={{ mt: 3, mb: 2, fontWeight: "bold" }}
                >
                    Entrar
                </Button>
                <Link component={RouterLink} to="/register" underline="hover">
                    Faça seu registro!
                </Link>
            </Box>
        </Paper>
    );
};

export default LoginForm;
