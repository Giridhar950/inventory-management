# Deployment Checklist

Use this checklist before deploying to production.

## ?? Security

- [ ] Change all default passwords
  - [ ] Admin password (from admin123)
  - [ ] Manager password (from manager123)
  - [ ] Cashier password (from cashier123)
- [ ] Update `SECRET_KEY` in backend/.env to a strong random string (min 32 characters)
- [ ] Set `DEBUG=False` in backend/.env
- [ ] Review and update `ALLOWED_ORIGINS` in backend/.env
- [ ] Update frontend `VITE_API_BASE_URL` to production URL
- [ ] Enable HTTPS/TLS for all connections
- [ ] Configure firewall rules (only allow ports 80, 443)
- [ ] Set up SSL certificates (Let's Encrypt recommended)

## ?? Database

- [ ] Use managed PostgreSQL service (RDS, Cloud SQL, Azure Database)
- [ ] Enable automated backups (daily minimum)
- [ ] Set up point-in-time recovery
- [ ] Enable connection encryption
- [ ] Create database user with minimal privileges
- [ ] Change default postgres password
- [ ] Enable query logging for audit

## ?? Application

- [ ] Build frontend for production (`npm run build`)
- [ ] Set up reverse proxy (Nginx)
- [ ] Configure rate limiting
- [ ] Set up CDN for static assets
- [ ] Enable gzip compression
- [ ] Configure logging (centralized logging recommended)
- [ ] Set up error tracking (Sentry, Datadog)
- [ ] Configure uptime monitoring
- [ ] Set up alerts for critical errors

## ?? CI/CD

- [ ] Set up automated testing
- [ ] Configure deployment pipeline
- [ ] Implement rollback strategy
- [ ] Set up staging environment
- [ ] Document deployment process

## ?? Monitoring

- [ ] Application performance monitoring
- [ ] Database performance monitoring
- [ ] Error tracking
- [ ] Uptime monitoring
- [ ] Resource usage alerts (CPU, memory, disk)
- [ ] Set up log aggregation

## ?? Access Control

- [ ] Disable root SSH access
- [ ] Use SSH keys instead of passwords
- [ ] Implement IP whitelisting for admin access
- [ ] Set up VPN for internal access
- [ ] Review and assign user roles properly
- [ ] Enable 2FA for admin accounts (if implemented)

## ?? Documentation

- [ ] Update README with production URLs
- [ ] Document backup/restore procedures
- [ ] Create incident response plan
- [ ] Document scaling procedures
- [ ] Create user training materials

## ?? Testing

- [ ] Load testing completed
- [ ] Security testing (OWASP Top 10)
- [ ] User acceptance testing
- [ ] Backup restoration tested
- [ ] Disaster recovery tested

## ?? Optional Enhancements

- [ ] Set up email notifications
- [ ] Configure SMS alerts
- [ ] Implement audit log retention policy
- [ ] Set up data archival strategy
- [ ] Configure auto-scaling (if using cloud)

## ?? Pre-Launch Verification

**Day Before Launch:**
- [ ] All secrets rotated
- [ ] Backups verified
- [ ] Monitoring alerts tested
- [ ] SSL certificate valid
- [ ] DNS records updated
- [ ] User accounts created
- [ ] Documentation reviewed

**Launch Day:**
- [ ] Monitor application closely
- [ ] Check error logs
- [ ] Verify all functionality
- [ ] Test from multiple locations
- [ ] Confirm backups running
- [ ] Monitor resource usage

## ?? Support Contacts

- **DevOps**: _______________
- **Database Admin**: _______________
- **Security Team**: _______________
- **On-Call**: _______________

## ?? Success Metrics

Track these after deployment:
- [ ] System uptime > 99.5%
- [ ] API response time < 500ms
- [ ] Zero critical security issues
- [ ] User satisfaction score > 4/5
- [ ] Successful daily backups

---

## Quick Commands

### Check Application Health
```bash
# Backend
curl https://api.yourdomain.com/health

# Frontend
curl https://yourdomain.com
```

### View Logs
```bash
# Docker
docker-compose logs -f backend
docker-compose logs -f frontend

# System logs (if not using Docker)
journalctl -u shopping-mart-backend -f
```

### Restart Services
```bash
docker-compose restart backend
docker-compose restart frontend
```

### Database Backup
```bash
docker-compose exec postgres pg_dump -U postgres shopping_mart > backup_$(date +%Y%m%d).sql
```

---

**Remember**: Always test changes in staging before deploying to production!

**Good luck with your deployment! ??**
