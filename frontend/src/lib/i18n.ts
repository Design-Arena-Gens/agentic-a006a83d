import i18n from "i18next";
import { initReactI18next } from "react-i18next";

const resources = {
  "pt-BR": {
    translation: {
      welcome: "Bem-vindo(a) ao EsthetiManage",
      tagline: "Automação inteligente para clínicas de estética.",
      dashboard: "Dashboard",
      patient_portal: "Portal do Paciente",
      admin_panel: "Painel Administrativo",
      appointments: "Agendamentos",
      revenue: "Receita",
      patients: "Pacientes",
      book_session: "Agendar sessão",
      submit: "Enviar",
    },
  },
};

if (!i18n.isInitialized) {
  i18n.use(initReactI18next).init({
    resources,
    lng: "pt-BR",
    fallbackLng: "pt-BR",
    interpolation: { escapeValue: false },
  });
}

export default i18n;
