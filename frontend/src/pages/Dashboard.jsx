import React, { useState } from 'react';
import { NavLink, Outlet, useNavigate } from 'react-router-dom';
import pinnacleLogo from '../images/PinnacleBrandMark.png';
import showIcon from '../images/show.svg';
import hideIcon from '../images/hide.svg';
import searchIcon from '../images/search.svg';
import carriersIcon from '../images/carriers.svg';
import settingsIcon from '../images/settings.svg';

const Dashboard = ({ handleLogout }) => {
    const navigate = useNavigate();
    const [isCollapsed, setIsCollapsed] = useState(false);

    const toggleSidebar = () => {
        setIsCollapsed(!isCollapsed);
    };

    return (
        <div className="dashboard-layout">
            <aside className={`sidebar ${isCollapsed ? 'collapsed' : ''}`}>
                <div className="sidebar-header">
                    <a href="/dashboard" className="logo-link">
                        <img src={pinnacleLogo} alt="Pinnacle Partners" className="sidebar-logo" />
                    </a>
                    <button className="sidebar-toggle" onClick={toggleSidebar} title={isCollapsed ? 'Expand sidebar' : 'Collapse sidebar'}>
                        <img src={isCollapsed ? showIcon : hideIcon} alt="Toggle" className="toggle-icon-img" />
                    </button>
                </div>

                <nav className="sidebar-nav">
                    <NavLink to="/dashboard" end className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                        <img src={searchIcon} alt="" className="icon" />
                        <span className="nav-text">Opportunities</span>
                    </NavLink>

                    <NavLink to="/dashboard/carriers" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                        <img src={carriersIcon} alt="" className="icon" />
                        <span className="nav-text">Carriers</span>
                    </NavLink>

                    <NavLink to="/dashboard/settings" className={({ isActive }) => isActive ? 'nav-item active' : 'nav-item'}>
                        <img src={settingsIcon} alt="" className="icon" />
                        <span className="nav-text">Settings</span>
                    </NavLink>
                </nav>

                <div className="sidebar-footer">
                    <button className="btn-logout" onClick={() => { handleLogout(); navigate('/'); }}>
                        <svg className="icon" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M17 7L15.59 8.41L18.17 11H8V13H18.17L15.59 15.58L17 17L22 12L17 7ZM4 5H12V3H4C2.9 3 2 3.9 2 5V19C2 20.1 2.9 21 4 21H12V19H4V5Z" fill="currentColor" />
                        </svg>
                        <span className="nav-text">Log Out</span>
                    </button>
                </div>
            </aside>

            <main className={`dashboard-main ${isCollapsed ? 'sidebar-collapsed' : ''}`}>
                <div className="dashboard-content">
                    <Outlet />
                </div>
            </main>
        </div>
    );
};

export default Dashboard;
