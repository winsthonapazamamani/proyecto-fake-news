from flask import request
from app.controllers.base_controller import BaseController
from app.models.verification import Verification
from app.models.news_article import NewsArticle

class NewsController(BaseController):
    """Controller for news-related operations"""
    
    @classmethod
    def get_verifications(cls):
        """Get all Amallulla verifications with filtering and pagination"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            category = request.args.get('category')
            rating = request.args.get('rating')
            search = request.args.get('search')
            
            # Build query
            query = Verification.query
            
            # Apply filters
            if category:
                query = query.filter(Verification.categoria_afirmacion == category)
            if rating:
                query = query.filter(Verification.calificacion_amallulla == rating)
            if search:
                query = query.filter(
                    Verification.titulo_afirmacion.ilike(f'%{search}%') |
                    Verification.contenido_afirmacion.ilike(f'%{search}%')
                )
            
            # Get paginated results
            paginated_data = cls.paginated_response(
                query=query.order_by(Verification.created_at.desc()),
                page=page,
                per_page=per_page
            )
            
            return cls.success_response(
                data=paginated_data,
                message="Verifications retrieved successfully"
            )
            
        except Exception as e:
            return cls.error_response(f"Error retrieving verifications: {str(e)}", 500)
    
    @classmethod
    def get_verification(cls, verification_id):
        """Get specific verification by ID"""
        try:
            verification = Verification.query.get(verification_id)
            if not verification:
                return cls.error_response("Verification not found", 404)
            
            return cls.success_response(
                data=verification.to_dict(),
                message="Verification retrieved successfully"
            )
            
        except Exception as e:
            return cls.error_response(f"Error retrieving verification: {str(e)}", 500)
    
    @classmethod
    def create_article(cls):
        """Create a new news article for classification"""
        try:
            data = request.get_json()
            
            # Validate required fields
            is_valid, error_message = cls.validate_required_fields(
                data, ['title', 'content']
            )
            if not is_valid:
                return cls.error_response(error_message, 400)
            
            # Validate content length
            if len(data['title'].strip()) < 5:
                return cls.error_response("Title must be at least 5 characters long", 400)
            if len(data['content'].strip()) < 10:
                return cls.error_response("Content must be at least 10 characters long", 400)
            
            def create_article_operation():
                article = NewsArticle(
                    title=data['title'].strip(),
                    content=data['content'].strip(),
                    source=data.get('source'),
                    url=data.get('url'),
                    category=data.get('category')
                )
                db.session.add(article)
                return article
            
            success, result, message = cls.handle_database_operation(
                create_article_operation,
                "Article created successfully"
            )
            
            if success:
                return cls.success_response(
                    data=result.to_dict(),
                    message=message,
                    status_code=201
                )
            else:
                return cls.error_response(message, 500)
                
        except Exception as e:
            return cls.error_response(f"Error creating article: {str(e)}", 500)
    
    @classmethod
    def get_categories(cls):
        """Get available categories"""
        categories = [
            'POLITICA', 'SALUD', 'ECONOMIA', 'EDUCACION', 'SEGURIDAD',
            'CORRUPCION', 'REDES_SOCIALES', 'INTERNACIONAL', 'GOBIERNO',
            'CONGRESO', 'ELECCIONES', 'COVID19', 'VACUNAS', 'OTROS'
        ]
        
        return cls.success_response(
            data=categories,
            message="Categories retrieved successfully"
        )
    
    @classmethod
    def get_ratings(cls):
        """Get available rating types"""
        ratings = [
            'FALSO', 'VERDADERO', 'ENGAÑOSO', 'EXAGERADO',
            'SIN_EVIDENCIAS', 'CONTEXTO_ERRONEO', 'DESACTUALIZADO'
        ]
        
        return cls.success_response(
            data=ratings,
            message="Ratings retrieved successfully"
        )
    
    @classmethod
    def get_articles(cls):
        """Get all news articles with pagination"""
        try:
            page = request.args.get('page', 1, type=int)
            per_page = request.args.get('per_page', 10, type=int)
            
            query = NewsArticle.query.order_by(NewsArticle.created_at.desc())
            
            paginated_data = cls.paginated_response(
                query=query,
                page=page,
                per_page=per_page
            )
            
            return cls.success_response(
                data=paginated_data,
                message="Articles retrieved successfully"
            )
            
        except Exception as e:
            return cls.error_response(f"Error retrieving articles: {str(e)}", 500)
    
    @classmethod
    def get_article(cls, article_id):
        """Get specific article by ID"""
        try:
            article = NewsArticle.query.get(article_id)
            if not article:
                return cls.error_response("Article not found", 404)
            
            return cls.success_response(
                data=article.to_dict(),
                message="Article retrieved successfully"
            )
            
        except Exception as e:
            return cls.error_response(f"Error retrieving article: {str(e)}", 500)
        