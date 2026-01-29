"""
Módulo de conexão e operações com Supabase
"""
from supabase import create_client, Client
from typing import Optional, List, Dict, Any
import config


class Database:
    """Classe para gerenciar conexão e operações com Supabase"""
    
    def __init__(self):
        """Inicializa conexão com Supabase"""
        if not config.SUPABASE_URL or not config.SUPABASE_KEY:
            raise ValueError("SUPABASE_URL e SUPABASE_KEY devem estar definidas no .env")
        
        self.client: Client = create_client(config.SUPABASE_URL, config.SUPABASE_KEY)
    
    def get_client(self) -> Client:
        """Retorna o cliente Supabase"""
        return self.client
    
    # ========== OPERAÇÕES COM TIMES ==========
    
    def listar_times(self, apenas_ativos: bool = True) -> List[Dict[str, Any]]:
        """Lista todos os times cadastrados"""
        query = self.client.table('times').select('*')
        
        if apenas_ativos:
            query = query.eq('ativo', True)
        
        response = query.order('nome_time').execute()
        return response.data
    
    def buscar_time_por_id(self, time_id: str) -> Optional[Dict[str, Any]]:
        """Busca um time específico por ID"""
        response = self.client.table('times').select('*').eq('id', time_id).execute()
        return response.data[0] if response.data else None
    
    def criar_time(self, nome_time: str, nome_dono: str, 
                   email: Optional[str] = None, 
                   observacoes: Optional[str] = None) -> Dict[str, Any]:
        """Cria um novo time"""
        data = {
            'nome_time': nome_time,
            'nome_dono': nome_dono,
            'email': email,
            'observacoes': observacoes
        }
        response = self.client.table('times').insert(data).execute()
        return response.data[0]
    
    def atualizar_time(self, time_id: str, **kwargs) -> Dict[str, Any]:
        """Atualiza dados de um time"""
        response = self.client.table('times').update(kwargs).eq('id', time_id).execute()
        return response.data[0]
    
    def desativar_time(self, time_id: str) -> Dict[str, Any]:
        """Desativa um time (soft delete)"""
        return self.atualizar_time(time_id, ativo=False)
    
    # ========== OPERAÇÕES COM RODADAS ==========
    
    def listar_rodadas(self, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """Lista todas as rodadas"""
        query = self.client.table('rodadas').select('*')
        
        if status:
            query = query.eq('status', status)
        
        response = query.order('numero').execute()
        return response.data
    
    def buscar_rodada_por_numero(self, numero: int) -> Optional[Dict[str, Any]]:
        """Busca uma rodada específica por número"""
        response = self.client.table('rodadas').select('*').eq('numero', numero).execute()
        return response.data[0] if response.data else None
    
    def criar_rodada(self, numero: int, data_rodada: str, 
                     mes_referencia: int, ano_referencia: int,
                     status: str = 'aberta',
                     observacoes: Optional[str] = None) -> Dict[str, Any]:
        """Cria uma nova rodada"""
        data = {
            'numero': numero,
            'data_rodada': data_rodada,
            'mes_referencia': mes_referencia,
            'ano_referencia': ano_referencia,
            'status': status,
            'observacoes': observacoes
        }
        response = self.client.table('rodadas').insert(data).execute()
        return response.data[0]
    
    def atualizar_rodada(self, rodada_id: str, **kwargs) -> Dict[str, Any]:
        """Atualiza dados de uma rodada"""
        response = self.client.table('rodadas').update(kwargs).eq('id', rodada_id).execute()
        return response.data[0]
    
    # ========== OPERAÇÕES COM CLASSIFICAÇÕES ==========
    
    def listar_classificacoes_rodada(self, rodada_id: str) -> List[Dict[str, Any]]:
        """Lista classificações de uma rodada específica"""
        response = self.client.table('classificacoes')\
            .select('*, times(nome_time, nome_dono)')\
            .eq('rodada_id', rodada_id)\
            .order('posicao')\
            .execute()
        return response.data
    
    def criar_classificacao(self, time_id: str, rodada_id: str,
                           posicao: int, pontuacao: float,
                           valor_premio: float) -> Dict[str, Any]:
        """Cria uma nova classificação"""
        data = {
            'time_id': time_id,
            'rodada_id': rodada_id,
            'posicao': posicao,
            'pontuacao': pontuacao,
            'valor_premio': valor_premio
        }
        response = self.client.table('classificacoes').insert(data).execute()
        return response.data[0]
    
    def atualizar_classificacao(self, classificacao_id: str, **kwargs) -> Dict[str, Any]:
        """Atualiza uma classificação"""
        response = self.client.table('classificacoes').update(kwargs).eq('id', classificacao_id).execute()
        return response.data[0]
    
    def deletar_classificacao(self, classificacao_id: str):
        """Deleta uma classificação"""
        response = self.client.table('classificacoes').delete().eq('id', classificacao_id).execute()
        return response.data
    
    # ========== OPERAÇÕES COM PREMIAÇÕES ==========
    
    def listar_premiacoes(self) -> List[Dict[str, Any]]:
        """Lista todas as premiações"""
        response = self.client.table('premiacoes').select('*').order('posicao').execute()
        return response.data
    
    def buscar_premiacao_por_posicao(self, posicao: int) -> Optional[Dict[str, Any]]:
        """Busca valor da premiação por posição"""
        response = self.client.table('premiacoes').select('*').eq('posicao', posicao).execute()
        return response.data[0] if response.data else None
    
    # ========== VIEWS E RANKINGS ==========
    
    def get_ranking_geral(self) -> List[Dict[str, Any]]:
        """Retorna ranking geral acumulado"""
        response = self.client.table('vw_ranking_geral').select('*').execute()
        return response.data
    
    def get_ranking_mensal(self, mes: Optional[int] = None, 
                          ano: Optional[int] = None) -> List[Dict[str, Any]]:
        """Retorna ranking mensal"""
        query = self.client.table('vw_ranking_mensal').select('*')
        
        if mes:
            query = query.eq('mes_referencia', mes)
        if ano:
            query = query.eq('ano_referencia', ano)
        
        response = query.execute()
        return response.data
    
    def get_historico_time(self, time_id: str) -> List[Dict[str, Any]]:
        """Retorna histórico completo de um time"""
        response = self.client.table('vw_historico_times')\
            .select('*')\
            .eq('time_id', time_id)\
            .execute()
        return response.data


# Instância global do banco
db = Database()