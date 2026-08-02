import pygame
from translations import get_text

class Renderer:
    def __init__(self):
        # Retro Fonts
        self.fonts = {
            'title': pygame.font.SysFont("Courier New", 34, bold=True),
            'opt': pygame.font.SysFont("Courier New", 24),
            'ticker': pygame.font.SysFont("Courier New", 18, bold=True),
            'footer': pygame.font.SysFont("Courier New", 16, italic=True)
        }
        
        # Hintergrund-Gradient vorrendern (Cyberpunk / Retro Look)
        self.bg_surface = pygame.Surface((800, 600))
        for i in range(600):
            color = (10 + i//30, 15 + i//40, 35 + i//20)
            pygame.draw.line(self.bg_surface, color, (0, i), (800, i))
        
        # Grid Pattern
        for x in range(0, 800, 40):
            pygame.draw.line(self.bg_surface, (25, 35, 60), (x, 0), (x, 600))
        for y in range(0, 600, 40):
            pygame.draw.line(self.bg_surface, (25, 35, 60), (0, y), (800, y))
            
        # UI Box (Glassmorphism / Retro Terminal style)
        self.menu_box = pygame.Surface((600, 400), pygame.SRCALPHA)
        pygame.draw.rect(self.menu_box, (20, 25, 40, 210), (0, 0, 600, 400), border_radius=15)
        pygame.draw.rect(self.menu_box, (0, 255, 150, 100), (0, 0, 600, 400), 2, border_radius=15)

    def render(self, screen, current_menu, state):
        screen.blit(self.bg_surface, (0, 0))
        
        # Menu-Box
        screen.blit(self.menu_box, (100, 100))

        # Title
        if hasattr(current_menu, 'title'):
            title_surf = self.fonts['title'].render(current_menu.title, True, (0, 255, 150))
            screen.blit(title_surf, (150, 130))

        # Options
        if hasattr(current_menu, 'options') and hasattr(current_menu, 'current_index'):
            for i, opt in enumerate(current_menu.options):
                color = (255, 255, 255) if i == current_menu.current_index else (100, 120, 150)
                if i == current_menu.current_index:
                    # Cursor Highlight (pulsierend)
                    p_alpha = int(40 + 20 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
                    h_rect = pygame.Surface((520, 35), pygame.SRCALPHA)
                    pygame.draw.rect(h_rect, (0, 255, 150, p_alpha), (0, 0, 520, 35), border_radius=5)
                    screen.blit(h_rect, (140, 180 + i*40))
                
                # Check format of option
                opt_text = opt['text'] if isinstance(opt, dict) else str(opt)
                opt_surf = self.fonts['opt'].render(opt_text, True, color)
                screen.blit(opt_surf, (150, 185 + i*40))

        # Multi-Tasking Ticker (oben rechts)
        if state.is_developing and getattr(state, 'active_projects', []):
            first_ap = state.active_projects[0]
            prog = int((first_ap["progress"] / max(1, first_ap["total_weeks"])) * 100)
            prog = min(100, prog)
            proj_name = first_ap["project"].name if hasattr(first_ap["project"], 'name') else '???'
            count_suffix = f" (+{len(state.active_projects)-1})" if len(state.active_projects) > 1 else ""
            ticker_text = f"DEV: {proj_name}{count_suffix} - {prog}%"
            
            # Pulsierender Effekt
            alpha = int(155 + 100 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            t_box = pygame.Surface((230, 40), pygame.SRCALPHA)
            pygame.draw.rect(t_box, (0, 255, 150, alpha // 4), (0, 0, 230, 40), border_radius=10)
            screen.blit(t_box, (550, 20))
            t_surf = self.fonts['ticker'].render(ticker_text, True, (0, 255, 150))
            screen.blit(t_surf, (570, 30))

        # Footer Info
        cal_text = state.get_calendar_text() if getattr(state, 'company_name', None) else ""
        money_txt = f"{get_text('money_label')}: {state.money:,} EUR"
        if cal_text:
            money_txt += f" | {cal_text}"
        f_surf = self.fonts['footer'].render(money_txt, True, (200, 200, 200))
        screen.blit(f_surf, (110, 510))

        pygame.display.flip()
