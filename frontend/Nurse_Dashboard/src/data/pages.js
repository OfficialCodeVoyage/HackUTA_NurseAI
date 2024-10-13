
import OverviewImg from "../assets/img/pages/overview.jpg";
import TransactionsImg from "../assets/img/pages/transactions.jpg";
import SettingsImg from "../assets/img/pages/settings.jpg";
import ServerErrorImg from "../assets/img/pages/500.jpg";

import { Routes } from "../routes";


export default [
    {
        "id": 1,
        "name": "Overview",
        "image": OverviewImg,
        "link": Routes.DashboardOverview.path
    },
    {
        "id": 2,
        "name": "Transactions",
        "image": TransactionsImg,
        "link": Routes.Transactions.path
    },
    {
        "id": 3,
        "name": "Settings",
        "image": SettingsImg,
        "link": Routes.Settings.path
    },
    {
        "id": 10,
        "name": "500",
        "image": ServerErrorImg,
        "link": Routes.ServerError.path
    }
];