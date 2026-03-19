import { useState } from "react";
import { useNavigate, Link as RouterLink } from "react-router-dom";
import {
    Box,
    TextField,
    Button,
    Typography,
    Paper,
    Alert,
    Link,
} from "@mui/material";
import serviceAPI from "../services/mainService";

const RegisterForm = () => {
    const [username, setUsername] = useState("");
    const [email, setEmail] = useState("");
    const [name, setName] = useState("");
    const [surname, setSurname] = useState("");
    const [password, setPassword] = useState("");
    const [confirmPassword, setConfirmPassword] = useState("");

    const [error, setError] = useState("");
    const [success, setSuccess] = useState(false);

    const navigate = useNavigate();

    const handleSubmit = async (e: React.SubmitEvent<HTMLFormElement>) => {
        e.preventDefault();
        setError("");
        setSuccess(false);

        if (password !== confirmPassword) {
            setError("As senhas não coincidem.");
            return;
        }

        try {
            await serviceAPI.post("/users/register/", {
                username,
                email,
                name,
                surname,
                password,
            });

            setSuccess(true);

            setTimeout(() => {
                navigate("/login");
            }, 2000);
        } catch (err: any) {
            console.error("Erro no cadastro:", err);
            const errorMessage =
                err.response?.data?.username?.[0] ||
                err.response?.data?.email?.[0] ||
                "Erro ao criar conta. Verifique os dados e tente novamente.";
            setError(errorMessage);
        }
    };

    return (
        <Paper
            elevation={3}
            sx={{ p: 4, width: "100%", maxWidth: 400, borderRadius: 2 }}
        >
            <Paper elevation={3} sx={{ bgcolor: "#1976d2", mb: 3 }}>
                <Typography
                    variant="h4"
                    component="h1"
                    align="center"
                    gutterBottom
                    fontWeight="bold"
                    color="#ffffff"
                    sx={{ py: 1 }}
                >
                    TO DO LIST
                </Typography>
            </Paper>

            <Box component="form" onSubmit={handleSubmit} noValidate>
                <Typography
                    variant="h5"
                    component="h2"
                    align="center"
                    gutterBottom
                    fontWeight="bold"
                >
                    Criar Conta
                </Typography>

                {error && (
                    <Alert severity="error" sx={{ mb: 2 }}>
                        {error}
                    </Alert>
                )}
                {success && (
                    <Alert severity="success" sx={{ mb: 2 }}>
                        Conta criada com sucesso! Redirecionando...
                    </Alert>
                )}

                <TextField
                    margin="normal"
                    required
                    fullWidth
                    label="Nome de usuário (Username)"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
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
                    label="E-mail"
                    type="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
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
                    label="Nome"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
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
                    label="Sobrenome"
                    value={surname}
                    onChange={(e) => setSurname(e.target.value)}
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
                    label="Confirmar Senha"
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
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
                    disabled={success}
                    sx={{ mt: 3, mb: 2, fontWeight: "bold" }}
                >
                    Registrar
                </Button>

                <Box sx={{ textAlign: "center", mt: 2 }}>
                    <Typography variant="body2">
                        Já tem uma conta?{" "}
                        <Link
                            component={RouterLink}
                            to="/login"
                            underline="hover"
                        >
                            Faça login aqui
                        </Link>
                    </Typography>
                </Box>
            </Box>
        </Paper>
    );
};

export default RegisterForm;
