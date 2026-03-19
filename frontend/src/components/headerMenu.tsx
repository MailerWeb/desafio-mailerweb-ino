import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/authContext";
import { Link as RouterLink } from "react-router-dom";
import {
    AppBar,
    Box,
    Button,
    Toolbar,
    Typography,
    Tooltip,
} from "@mui/material";
import LogoutIcon from "@mui/icons-material/Logout";

const HeaderMenu = () => {
    const { logout } = useAuth();

    return (
        <AppBar position="sticky" elevation={2}>
            <Toolbar>
                <Typography
                    variant="h6"
                    component={RouterLink}
                    to="/home"
                    sx={{
                        textDecoration: "none",
                        color: "inherit",
                        fontWeight: "bold",
                        flexShrink: 0,
                    }}
                >
                    BOOKING
                    <br />
                    MANAGER
                </Typography>

                <Box
                    sx={{
                        flexGrow: 1,
                        display: "flex",
                        justifyContent: "center",
                        gap: 3,
                    }}
                >
                    <Button color="inherit" component={RouterLink} to="/home">
                        Início
                    </Button>
                    <Button color="inherit" component={RouterLink} to="/home">
                        Bookings
                    </Button>
                    <Button color="inherit" component={RouterLink} to="/home">
                        Rooms
                    </Button>
                </Box>

                <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                    <Box
                        sx={{
                            display: { xs: "none", sm: "flex" },
                            alignItems: "center",
                            gap: 1,
                        }}
                    >
                        <Typography variant="body2"></Typography>
                    </Box>

                    <Tooltip title="Sair">
                        <Button
                            color="inherit"
                            onClick={logout}
                            startIcon={<LogoutIcon />}
                            sx={{ fontWeight: "bold" }}
                        >
                            Sair
                        </Button>
                    </Tooltip>
                </Box>
            </Toolbar>
        </AppBar>
    );
};

export default HeaderMenu;
