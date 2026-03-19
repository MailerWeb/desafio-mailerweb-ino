import React, { createContext, useState, useEffect, useContext } from "react";
import serviceAPI from "../services/mainService";
import type { User } from "../type/user";

interface AuthContextType {
    user: User | null;
    login: (username_email: string, password: string) => Promise<void>;
    logout: () => void;
    loading: boolean;
}

const AuthContext = createContext<AuthContextType>({} as AuthContextType);

export function AuthProvider({ children }: { children: React.ReactNode }) {
    const [user, setUser] = useState<User | null>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const token = localStorage.getItem("token");
        const savedUser = localStorage.getItem("user");

        if (token && savedUser) {
            try {
                setUser(JSON.parse(savedUser));
            } catch (e) {
                console.error("Erro ao ler usuário do localStorage", e);
                localStorage.removeItem("user");
                localStorage.removeItem("token");
            }
        }
        setLoading(false);
    }, []);

    const login = async (username_email: string, password: string) => {
        const params = new URLSearchParams();

        params.append("username_email", username_email);
        params.append("password", password);

        const response = await serviceAPI.post("/users/login", params, {
            headers: {
                "Content-Type": "application/x-www-form-urlencoded",
            },
        });

        const { access_token, user: userData } = response.data;

        localStorage.setItem("token", access_token);
        localStorage.setItem("user", JSON.stringify(userData));

        setUser(userData);
    };

    const logout = () => {
        localStorage.removeItem("token");
        localStorage.removeItem("user");
        setUser(null);
    };

    return (
        <AuthContext.Provider value={{ user, login, logout, loading }}>
            {children}
        </AuthContext.Provider>
    );
}

export const useAuth = () => useContext(AuthContext);
